import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import app_globals
from pylons.decorators import jsonify

from chatroom.lib.base import BaseController, render
from datetime import datetime, timedelta
import time
import json
from chatroom.lib.response import *

log = logging.getLogger(__name__)

def _makeMessage(nickname, content, messageTime):
    return {"nickname": nickname ,
            "content": content,
            "timestamp": time.mktime(messageTime.timetuple()),
            "time": messageTime.strftime("%c")}

# Utilities
def _long_poll(q, pos):
    expired = datetime.now() + timedelta(0, 45);
    while expired >= datetime.now() and pos >= len(q):
        time.sleep(0.5)

def _no_poll(q, pos):
    return None

class MessageController(BaseController):

    def add(self):
        userId = 1
        content = request.params["content"]
        if "nickname" in session:
            nickname = session["nickname"]
        else:
            nickname = "Unknown"

        message = _makeMessage(nickname, content, datetime.now())
        log.info("New message: %s" % str(message))
        app_globals.messageQueue.append(message)

        if app_globals.messageDeliverer:
            app_globals.messageDeliverer.notify()

        return 'OK'

    @jsonify
    def update(self):
        return self._update_message()

    @jsonify
    def update_long_poll(self):
        log.info("Multithreading Update")
        return self._update_message(_long_poll)

    def _update_message(self, pending = _no_poll):
        app_globals.messageCounter.increase()
        log.info("Client poll Update.")
        q = app_globals.messageQueue

        size = len(q)
        pos = self._get_pos(size)

        pending(q, pos)

        size = len(q)
        if pos >= size:
            return make_success_response([]);

        session["pos"] = size
        session.save();
        app_globals.messageCounter.decrease()

        messages = q[pos:size]
        return make_success_response(messages);

    def _get_pos(self, size):
        if "pos" not in session:
            session["pos"] = size - 100 if size - 100 > 0 else 0
        return session["pos"]


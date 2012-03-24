import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import app_globals
from pylons.decorators import jsonify

from chatroom.lib.base import BaseController, render
from chatroom.lib.message import Message
from datetime import datetime, timedelta
import time
import json

log = logging.getLogger(__name__)

def _makeMessage(nickname, content, time = datetime.now()):
    return {"nickname": nickname , "content": content, "time": str(time)}

# Utilities
def _long_poll(q, pos):
    # TODO:
    expired = datetime.now() + timedelta(0, 10);
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

        message = _makeMessage(nickname, content)
        app_globals.messageQueue.append(message)

        return 'OK'

    @jsonify
    def update(self):
        return self._update_message()

    @jsonify
    def update_long_poll(self):
        return self._update_message(_long_poll)

    def _update_message(self, pending = _no_poll):
        q = app_globals.messageQueue
        if "pos" not in session:
            session["pos"] = 0

        size = len(q)
        pos = session["pos"]

        pending(q, pos)

        if pos >= size:
            return []

        session["pos"] = size
        session.save();

        messages = q[pos:size]
        return messages

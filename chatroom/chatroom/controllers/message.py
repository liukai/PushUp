import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import app_globals
from pylons.decorators import jsonify

from chatroom.lib.base import BaseController, render
from chatroom.lib.message import Message
from datetime import datetime, timedelta
import time

log = logging.getLogger(__name__)

def makeMessage(userId, content, time = datetime.now()):
    return {"id": userId , "content": content, "time": str(time)}

class MessageController(BaseController):

    def add(self):
        userId = 1
        content = request.params["content"]

        message = makeMessage(userId, content)
        app_globals.messageQueue.append(message)

        return 'OK'

    @jsonify
    def update(self):
        q = app_globals.messageQueue
        size = len(q)
        if "pos" not in session:
            session["pos"] = 0
        pos = session["pos"]
        session.save();
        if pos >= size:
            return []

        session["pos"] = size
        return q[pos:]

    @jsonify
    def update_long_poll(self):
        q = app_globals.messageQueue
        if "posit" not in session:
            session["posit"] = 0
        pos = session["posit"]

        expired = datetime.now() + timedelta(0, 10);
        while expired >= datetime.now() and pos >= len(q):
            time.sleep(0.5)

        size = len(q)
        if pos <= size:
            session["posit"] = size
            session.save();

            return q[pos:size]
        else:
            return []

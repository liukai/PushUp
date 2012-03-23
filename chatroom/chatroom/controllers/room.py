import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from chatroom.lib.base import BaseController, render
from pylons import app_globals

log = logging.getLogger(__name__)

_pollMethods = ["client", "multithread", "event"]
_defaultMethod = _pollMethods[0]

class RoomController(BaseController):

    def chat(self):
        if self._tryJoin() or self._hasCheckedIn():
            c.polling = self._pollingMethod()
            c.nickname = session["nickname"]
            return render('/chat.mako')

        return render('/join.mako')

    def leave(self):
        if "nickname" in session:
            del session["nickname"]
        return render('/join.mako')

    def _pollingMethod(self):
        if "polledBy" not in request.params:
            return _defaultMethod

        method = request.params["polledBy"]
        if method not in _pollMethods:
            return _defaultMethod

        return method
    def _tryJoin(self):
        if "nickname" not in request.params:
            return False;

        session["nickname"] = request.params["nickname"]
        session["pos"] = 0
        session.save()

    def _hasCheckedIn(self):
        return "nickname" in session


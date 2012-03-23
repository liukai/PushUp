import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from chatroom.lib.base import BaseController, render
from pylons import app_globals

log = logging.getLogger(__name__)

class RoomController(BaseController):

    def chat(self):
        return  render('/chat.mako') if self._hasCheckedIn() \
                else render('/join.mako')

    def _hasCheckedIn(self):
        return "nickname" not in session


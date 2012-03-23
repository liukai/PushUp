import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from chatroom.lib.response import *
from chatroom.lib.base import BaseController, render
from pylons.decorators import jsonify

log = logging.getLogger(__name__)

class UsersController(BaseController):
    @jsonify
    def join(self):
        if "nickname" not in request.params:
            return make_error_response("expected nickname in the request")

        nickname = request.params["nickname"]
        session["nickname"] = nickname
        session["pos"] = 0

        response = make_success_response({"nickname": nickname})

        return response

    @jsonify
    def leave(self):
        del session["nickname"]
        del session["pos"]

        return make_success_response({})

from chatroom.tests import *

class TestRoomController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='room', action='index'))
        # Test response...

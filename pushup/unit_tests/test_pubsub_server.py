import unittest
import sys

sys.path.append("..")
from pubsub_server import *

class PubSubServerTest(unittest.TestCase):
    def test_normalize(self):
        resFormat = '{"result": "ok", "data": %s, "max_id": %d}'
        factory = PubSubFactory(0, 0, resFormat)

        messages = []
        self.assertEqual('{"result": "ok", "data": [], "max_id": 0}',
                         factory._normalize(messages))
        messages.append((1, "1"))
        self.assertEqual('{"result": "ok", "data": [1], "max_id": 1}',
                         factory._normalize(messages))
        messages.append((2, "2"))
        self.assertEqual('{"result": "ok", "data": [1,2], "max_id": 2}',
                         factory._normalize(messages))


if __name__ == "__main__":
    unittest.main()

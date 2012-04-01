import unittest
import sys
import time
sys.path.append("..")

from pubsub import PubSub, Channel

class ChannelTest(unittest.TestCase):
    def test_publish(self):
        messages = []
        onReceive = lambda m: self._onReceive(messages, m)

        c = Channel(10)
        self.assertEqual(0, len(c.messageQueue))
        c.subscribe(onReceive, None)
        self.assertEqual(0, len(messages))

        c.publish("data1")
        c.publish("data2")
        self.assertEqual(1, len(c.messageQueue))
        c.subscribe(onReceive, None)
        self.assertEqual(2, len(messages))

        time.sleep(1)
        c.publish("data3")
        self.assertEqual(2, len(c.messageQueue))
        c.subscribe(onReceive, None)
        self.assertEqual(3, len(messages))
        self.assertEqual("['data1', 'data2', 'data3']", str(messages))

    def test_subscriber_notification(self):
        messages = []
        Timeout = True
        onReceive = lambda m: self._onReceive(messages, m)
        onTimeout = lambda: self._onTimeout(messages)

        c = Channel(10)

        self.assertEqual(0, len(c.subscribers))
        c.subscribe(onReceive, None, waitForSeconds = 1)
        self.assertEqual(1, len(c.subscribers))

        c.publish("data", False)
        self.assertEqual("data", "".join(messages))
        self.assertEqual(0, len(c.subscribers))

    def test_purge_message(self):
        c = Channel(1)

        self.assertEqual(0, len(c.messageQueue))
        c.publish("data")
        self.assertEqual(1, len(c.messageQueue))
        c.purgeMessageQueue()
        self.assertEqual(1, len(c.messageQueue))

        time.sleep(1)
        c.purgeMessageQueue()
        self.assertEqual(0, len(c.messageQueue))

    def test_purge_subscribers(self):
        c = Channel(1)
        messages = []
        onTimeout = lambda: self._onTimeout(messages)

        self.assertEqual(0, len(c.subscribers))
        c.subscribe(None, onTimeout, waitForSeconds = 1)
        self.assertEqual(1, len(c.subscribers))
        c.purgeSubscribers()
        self.assertEqual(1, len(c.subscribers))
        self.assertEqual(0, len(messages))

        time.sleep(1)
        print c.subscribers
        c.purgeSubscribers()
        self.assertEqual(0, len(c.subscribers))
        self.assertEqual("timeout", messages[0])

    def _onReceive(self, messages1, messages2):
        del messages1[:]
        messages1.extend(messages2)

    def _onTimeout(self, message):
        message.append("timeout")


class PubsubTest(unittest.TestCase):
    def test_publish(self):
        pubsub = PubSub(10)
        self.assertEqual(0, len(pubsub.channels))

        pubsub.publish("channel", "data")
        self.assertEqual(1, len(pubsub.channels))
        self.assertTrue("channel" in pubsub.channels)

        pubsub.publish("channel2", "data")
        self.assertEqual(2, len(pubsub.channels))
        self.assertTrue("channel2" in pubsub.channels)

if __name__ == "__main__":
    unittest.main()

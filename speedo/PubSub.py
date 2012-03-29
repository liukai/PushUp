import sys
from twisted.internet import reactor, task
from bintrees.rbtree import RBTree

from util import now, toUnixTime, partition

class PubSub:
    def __init__(self, validFor):
        self.messages = RBTree()
        self.validFor = validFor
        self.channels = {}

        # Start looping call for message purging
        purgeMessages = lambda: self.purge(self.messages, self.validFor)
        purgeMessagesLoopingCall = task.LoopingCall(purgeMessages)
        purgeMessagesLoopingCall.start(1, False)

        # Start looping call for subscriber purging
        purgeSubscribersLoopingCall = \
                task.LoopingCall(self._purgeSubscribers)
        purgeSubscribersLoopingCall.start(1, False)

    def publish(self, channel, data):
        time = now()
        self.messages.setdefault(time, []).append(data)
        self._notify(channel, time, data)

    def subscribe(self, channel, callback,
                  timeFrom = 0, timeTo = sys.maxint,
                  waitForSeconds = 0):
        if channel not in self.channels:
            messages = []
        else:
            messages = list(self.channels[chanel][timeFrom: timeTo])
        if len(messages) != 0 or waitForSeconds == 0:
            callback(messages)
            return

        waitUntil = now() + waitForSeconds
        value = (timeFrom, timeTo, callback)

        subscribers = self.channels.setdefault(channel, RBTree())
        subscribers.setdefault(waitUntil, []).append(value)

    def purge(self, timedItems, validFor):
        expired = now() - validFor
        del timedItems[:expired]

    def _notify(self, channel, time, data):
        if channel not in self.channels:
            return

        channel = self.channels[channel]
        self.purge(channel, 0)

        for key, subscribers in channel.items():
            index = partition(subscribers,
                              lambda sub: time < sub[0] or time > sub[1])

            for i in range(index, len(subscribers)):
                reactor.callLater(0, subscribers[i][2], data)
            del subscribers[index:]
            if len(subscribers) == 0:
                del channel[key]

    def _purgeSubscribers(self):
        for channel in self.channels:
            self.purge(channel, 0)

# TODO: ths is an ad-hoc test and will be removed 
# in the future.
if __name__ == "__main__":
    tree = PubSub(5)

    def h(data):
        print "haha"
    def hh(data):
        print "hehe"
    tree.subscribe(1, h)
    tree.subscribe(1, hh)

    tree.publish(1, 1)
    tree.publish(1, 2)
    tree.publish(1, 3)
    tree.publish(1, 4)


    reactor.run()

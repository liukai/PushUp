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

    def subscribe(self, channel, onReceive, onTimeout,
                  timeFrom = 0, timeTo = sys.maxint,
                  waitForSeconds = 0):
        if channel not in self.channels:
            messages = []
        else:
            messages = list(self.channels[channel][timeFrom: timeTo])


        if len(messages) != 0 or waitForSeconds == 0:
            onReceive(messages)
            return

        waitUntil = now() + waitForSeconds
        value = (timeFrom, timeTo, onReceive, onTimeout)

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
        current = now()
        for _, channel in self.channels.items():
            for _, subscribers in channel[:current].items():
                for sub in subscribers:
                    reactor.callLater(0, sub[3])
            del channel[:current]

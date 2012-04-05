import sys
from twisted.internet import reactor, task
from bintrees.rbtree import RBTree

from util import now, toUnixTime, partition, IdGenerator

class Channel:
    def __init__(self, expiredIn):
        self.messageQueue = RBTree()
        self.subscribers = RBTree()
        self.expiredIn = expiredIn
        self.idGenerator = IdGenerator()

        task.LoopingCall(self.purgeMessageQueue).start(1, False)
        task.LoopingCall(self.purgeSubscribers).start(1, False)

    def publish(self, data, isAsync = True):
        time = now()
        dataWithId = (self.idGenerator.generateId(), data)
        self.messageQueue.setdefault(time, []).append(dataWithId)
        self.notify(time, dataWithId, isAsync)

    # TODO: should rename to: subscribeByTime
    def subscribe(self, onReceive, onTimeout,
                  timeFrom = 0, timeTo = sys.maxint,
                  minId = 0, waitForSeconds = 0):
        messages = self._flatten(self.messageQueue[timeFrom: timeTo], minId)
        messages = list(messages)
        print messages

        if len(messages) != 0 or waitForSeconds == 0:
            onReceive(messages)
            return

        waitUntil = now() + waitForSeconds
        value = (timeFrom, timeTo, onReceive, onTimeout)

        subscribers = self.subscribers.setdefault(waitUntil, []).append(value)

    def notify(self, time, data, isAsync = True):
        # purge expired subscribers
        self.purgeSubscribers()

        for time, bucket in self.subscribers.items():
            index = partition(bucket,
                              lambda sub: time < sub[0] or time > sub[1])

            data = [data]
            for i in range(index, len(bucket)):
                callback = bucket[i][2]
                if isAsync:
                    reactor.callLater(0, callback, data)
                else:
                    callback(data)

            del bucket[index:]

            if len(bucket) == 0:
                del self.subscribers[time]

    def purgeMessageQueue(self):
        expired = now() - self.expiredIn + 1
        del self.messageQueue[:expired]

    def purgeSubscribers(self):
        expired = now() + 1
        for data in self._flatten(self.subscribers[:expired], 0):
            data[3]()
        del self.subscribers[:expired]

    # --- Utilities ---
    def _flatten(self, buckets, minId):
        for bucket in buckets.values():
            for item in bucket:
                if item[0] >= minId:
                    yield item

class PubSub:
    def __init__(self, expiredIn):
        self.expiredIn = expiredIn
        self.channels = {}

    def publish(self, channel, data):
        if channel not in self.channels:
            self.channels[channel] = Channel(self.expiredIn)
        self.channels[channel].publish(data)

    def subscribe(self, channel, onReceive, onTimeout,
                  timeFrom = 0, timeTo = sys.maxint, minId = 0,
                  waitForSeconds = 0):
        if channel not in self.channels:
            self.channels[channel] = Channel(self.expiredIn)
        self.channels[channel].subscribe(onReceive, onTimeout,
                                         timeFrom, timeTo,
                                         minId,
                                         waitForSeconds)
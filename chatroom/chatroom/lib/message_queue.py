import redis
from datetime import datetime, timedelta
from time import mktime
import threading
import time

class RedisMessageQueue:
    def __init__(self, queueName, host = "localhost", port = 6379):
        self.queueName = queueName
        self.chanel = queueName + ":chanel"

        #self.connection_pool = redis.ConnectionPool()
        self.redisServer = redis.Redis(host, port)
        self.pubsub = self.redisServer.pubsub()

    def push(self, user, message, timestamp = datetime.now()):
        # convert time to number
        timestamp = self._to_unix_time(timestamp)
        message = self._to_message(user, message, timestamp)

        # add to the sorted set
        self.redisServer.zadd(self.queueName, message, timestamp)

        # publish to the chanel
        self.redisServer.publish(self.chanel, message)

    def purge(self, beforeTimestamp):
        beforeTimestamp= self._to_unix_time(beforeTimestamp)
        self.redisServer.zremrangebyscore(self.queueName, "-inf", beforeTimestamp)

    def range(self, afterTimestamp, waitForSeconds = 0):
        afterTimestamp= self._to_unix_time(afterTimestamp)
        messages =  self.redisServer.zrangebyscore(self.queueName, afterTimestamp, "+inf")

        if len(messages) > 0 or waitForSeconds == 0:
            return messages

        # Wait until message arrives
        thread = threading.Thread(target=RedisMessageQueue._listen,
                                   args=(self, messages, afterTimestamp))
        # thread.daemon = True
        thread.start()
        thread.join(waitForSeconds)

        terminateMessage = "TERMINATE%d" % thread.ident
        self.redisServer.publish(self.chanel, terminateMessage)

        return messages

    def _listen(self, messages, afterTimestamp):
        self.pubsub.subscribe(self.chanel)
        terminateMessage = "TERMINATE%d" % threading.current_thread().ident
        incomingMessage = None
        while incomingMessage != terminateMessage:
            incomingMessage = self.pubsub.listen().next()['data']
            if not incomingMessage.startswith("TERMINATE"):
                break

        newMessage =  self.redisServer.zrangebyscore(self.queueName,
                                                     afterTimestamp, "+inf")
        messages.extend(newMessage)

    def _to_message(self, user, message, timestamp):
        return "%d:%s:%s" % (timestamp, user, message)

    def _to_unix_time(self, timestamp):
        return mktime(timestamp.timetuple()) * 1.0

q = RedisMessageQueue("queue:big")
print q.range(datetime.now(), 10)

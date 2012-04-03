from twisted.internet import protocol
from twisted.protocols import basic
from pubsub import PubSub
import urlparse
import exceptions
import sys
from util import *

class PubSubProtocol(basic.LineReceiver):
    def lineReceived(self, line):
        print 'LINE', line
        parts = line.split('\t', 1)
        channel = int(parts[0])
        message = parts[1]
        self.factory.pubsub.publish(channel, message)

class PubSubFactory(protocol.ServerFactory):
    protocol = PubSubProtocol

    def __init__(self, validFor, subscriptionValidFor, messageFormat):
        self.pubsub = PubSub(validFor)
        self.subscriptionValidFor = subscriptionValidFor
        self.messageFormat = messageFormat

    def subscribe(self, request):
        urlComponents = urlparse.urlparse(request.uri)
        query = urlparse.parse_qs(urlComponents.query)

        if "channel" not in query:
            self._reportError(request)
            return

        channel = tryParseInt(query["channel"][0], 0)
        if channel == 0:
            self._reportError(request)
            return

        query.setdefault("time_from", [0])
        timeFrom = tryParseInt(query["time_from"][0], 0)

        query.setdefault("min_id", [0])
        mid = tryParseInt(query["min_id"][0], 0)

        notify = lambda message: self._notify(
                request,message)
        print "parameters", timeFrom, mid
        self.pubsub.subscribe(channel, notify,
                              request.finish,
                              timeFrom,
                              minId = mid,
                              waitForSeconds = self.subscriptionValidFor)

    def _notify(self, request, message):
        try:
            request.setResponseCode(200, "OK")
            message = self._normalize(message)
            print "MESSAGE: ", message
            request.write(message)
            request.finish()
        except Exception as e:
            print "Unhandled Error"
            print e

    def _normalize(self, messages):
        if len(messages) == 0:
            return self.messageFormat % ("[]", 0)

        maxId = messages[-1][0]
        messages = (m for id, m in messages)
        messages = "[%s]" % ",".join(messages)

        return self.messageFormat % (messages, maxId)

    def _reportError(self, request):
        request.setResponseCode(400, "error")
        request.responseHeaders.addRawHeader("Content-Type",
                                             "text/html")
        request.write("<H1>Error</H1>")
        request.write(
                "<p>Invalid channel format in query</p>")
        request.finish()


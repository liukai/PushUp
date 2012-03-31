from twisted.internet import protocol
from twisted.protocols import basic
from pubsub import PubSub
import urlparse
import exceptions
import sys

class PubSubProtocol(basic.LineReceiver):
    def lineReceived(self, line):
        parts = line.split('\t', 1)
        channel = int(parts[0])
        message = parts[1]
        self.factory.pubsub.publish(channel, message)

class PubSubFactory(protocol.ServerFactory):
    protocol = PubSubProtocol

    def __init__(self, validFor):
        self.pubsub = PubSub(validFor)

    def subscribe(self, request):
        urlComponents = urlparse.urlparse(request.uri)
        query = urlparse.parse_qs(urlComponents.query)

        if "channel" not in query:
            self._reportError(request)
            return

        channel = self._tryParse(query["channel"][0])
        if channel == 0:
            self._reportError(request)
            return

        query.setdefault("time_from", 0)
        timeFrom = self._tryParse(query["time_from"])
        print "time from", timeFrom

        notify = lambda message: self._notify(
                request,message)
        self.pubsub.subscribe(channel, notify,
                              request.finish,
                              timeFrom,
                              waitForSeconds = 5) # TODO

    def _notify(self, request, message):
        request.setResponseCode(200, "OK")
        request.responseHeaders.addRawHeader("Content-Type",
                                             "text/html")
        request.write("<H1>It works!</H1>")
        request.finish()

    def _reportError(self, request):
        request.setResponseCode(400, "error")
        request.responseHeaders.addRawHeader("Content-Type",
                                             "text/html")
        request.write("<H1>Error</H1>")
        request.write(
                "<p>Invalid channel format in query</p>")
        request.finish()

    def _tryParse(self, text):
        try:
            return int(text)
        except Exception:
            return 0


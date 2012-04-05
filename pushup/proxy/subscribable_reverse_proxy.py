from reverse_proxy import *
from twisted.internet import reactor, task
from twisted.web.http import Request
from twisted.web.server import NOT_DONE_YET
from urllib import quote as urlquote

import urlparse

# -- Long Polling support reverse proxy --
class SubscribableReverseProxy(ReverseProxyResource):
    def __init__(self, host, port, path,
                 inceptedPaths = [], myReactor = reactor):
        ReverseProxyResource.__init__(self, host, port, path, myReactor)

        # checkTime in seconds to check app for new data
        self.checkTime = 0.2
        self.delayedRequests = []
        self.forwardRequest = None

        # Setup looping calls
        loopingRequestCheck = task.LoopingCall(self.processDelayedRequests)
        loopingRequestCheck.start(0.2, False)
        self.inceptedPaths = inceptedPaths

    def getChild(self, path, request):
        """
        Create and return a proxy resource with the same proxy configuration
        as this one, except that its path also contains the segment given by
        C{path} at the end.
        """
        proxy = SubscribableReverseProxy(
            self.host, self.port,
            self.path + '/' + urlquote(path, safe=""),
            self.inceptedPaths,
            self.reactor)
        proxy.forwardRequest = self.forwardRequest
        return proxy

    def render(self, request):
        urlComponents = urlparse.urlparse(request.uri)
        if urlComponents.path in self.inceptedPaths:
            self.delayedRequests.append(request)
            return NOT_DONE_YET

        return ReverseProxyResource.render(self, request)

    def processDelayedRequests(self):
        """
        Processes the delayed requests that did not have
        any data to return last time around.
        """
        assert self.forwardRequest != None

        # run through delayed requests
        for request in self.delayedRequests:
            try:
                self.forwardRequest(request)
            except Exception as e:
                print e
            finally:
                self.delayedRequests.remove(request)

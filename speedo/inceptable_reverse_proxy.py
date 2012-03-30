from reverse_proxy import *

# -- Long Polling support reverse proxy --
class LongPollingReverseProxyResource(ReverseProxyResource):
    def __init__(self, host, port, path, reactor=reactor):
        ReverseProxyResource.__init__(self, host, port, path, reactor)

        # throttle in seconds to check app for new data
        self.throttle = 0.2
        self.delayed_requests = []

        # Setup looping calls
        loopingCall = task.LoopingCall(self.processDelayedRequests)
        loopingCall.start(0.2, False)
        self.longPollingPaths = []

    def getChild(self, path, request):
        """
        Create and return a proxy resource with the same proxy configuration
        as this one, except that its path also contains the segment given by
        C{path} at the end.
        """
        resource = LongPollingReverseProxyResource(
            self.host, self.port,
            self.path + '/' + urlquote(path, safe=""),
            self.reactor)
        resource.longPollingPaths = self.longPollingPaths

        return resource
    def render(self, request):
        path = urlparse.urlparse(request.uri).path
        if path in self.longPollingPaths:
            self.delayed_requests.append(request)
            return NOT_DONE_YET

        return ReverseProxyResource.render(self, request)

    def processDelayedRequests(self):
        """
        Processes the delayed requests that did not have
        any data to return last time around.
        """
        # run through delayed requests
        for request in self.delayed_requests:
            try:
                # TODO: SAMPLE CODE
                request.setResponseCode(200, "OK")
                request.responseHeaders.addRawHeader("Content-Type",
                                                     "text/html")
                request.write("<H1>Message Intercepted</H1>")
                request.write("<p>hello world</p>")
                request.finish()
            except:
                pass
            finally:
                self.delayed_requests.remove(request)

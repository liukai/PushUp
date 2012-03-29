from twisted.internet import reactor, protocol
from twisted.web import server
from reverse_proxy import LongPollingReverseProxyResource
import config
from twisted.protocols import basic

# TODO
#   * Add long polling expired time
#   * How to generalize this proxy?
#   * two threads are needed
#       - reverse proxy for clients
#       - receiving messages the proxied server

# TODO: the following protocoal is not finished.
# It will be moved to another file
class PubSubProtocol(basic.LineReceiver):
    def lineReceived(self, line):
        self.transport.write(line)
        self.transport.loseConnection()

class PubSubFactory(protocol.ServerFactory):
    protocol = PubSubProtocol

    def __init__(self):
        pass


def main():
    # Start reverse Proxy
    proxiedServerPort = config.PROXIED_SERVER["port"]
    proxiedServerHost = config.PROXIED_SERVER["host"]
    resource = LongPollingReverseProxyResource(proxiedServerHost,
                                               proxiedServerPort, '')
    resource.longPollingPaths = config.LONG_POLLING_PATHS
    site = server.Site(resource)

    listenClientPort = config.SERVER["listen_client_port"]
    reactor.listenTCP(listenClientPort, site)

    # Start Pub/Sub
    listenBackendPort = config.SERVER["listen_backend_port"]
    reactor.listenTCP(listenBackendPort, PubSubFactory())
    reactor.run()

if __name__ == "__main__":
    main()

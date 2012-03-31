from pubsub_server import PubSubFactory
from long_polling_proxy import LongPollingProxy
from twisted.internet import reactor, protocol
from twisted.protocols import basic
from twisted.web import server
import config

def main():
    # Start Pub/Sub
    listenBackendPort = config.SERVER["listen_backend_port"]
    pubSubFactory = PubSubFactory(config.PUBSUB["valid_for"])
    reactor.listenTCP(listenBackendPort, pubSubFactory)

    # Start reverse Proxy
    proxiedServerPort = config.PROXIED_SERVER["port"]
    proxiedServerHost = config.PROXIED_SERVER["host"]
    proxy = LongPollingProxy(proxiedServerHost,\
                             proxiedServerPort, '',
                             config.LONG_POLLING_PATHS)

    proxy.forwardRequest = pubSubFactory.subscribe
    site = server.Site(proxy)

    listenClientPort = config.SERVER["listen_client_port"]
    reactor.listenTCP(listenClientPort, site)

    reactor.run()

if __name__ == "__main__":
    main()

from pubsub.pubsub_server import PubSubFactory
from proxy.subscribable_reverse_proxy import SubscribableReverseProxy
from twisted.internet import reactor, protocol
from twisted.protocols import basic
from twisted.web import server
import config

def main():
    pubSubFactory = startPubSub(config.PUBLISH)
    startReverseProxy(config.REVERSE_PROXY, pubSubFactory.subscribe)

    reactor.run()

def startPubSub(config):
    port = config["port"]
    expiredIn = config["expiredIn"]
    messageFormat = config["message_format"]
    waitFor = config["wait_for"]

    pubSubFactory = PubSubFactory(expiredIn, waitFor, messageFormat)
    reactor.listenTCP(port, pubSubFactory)

    return pubSubFactory

def startReverseProxy(config, forwardRequest):
    proxiedHost = config["proxied_host"]
    port = config["port"]
    subscriptionPath = config["subscription_path"]

    proxy = SubscribableReverseProxy(proxiedHost[0], proxiedHost[1],
                             '', subscriptionPath);

    proxy.forwardRequest = forwardRequest
    site = server.Site(proxy)

    reactor.listenTCP(port, site)


if __name__ == "__main__":
    main()


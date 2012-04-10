from pubsub.pubsub_server import PubSubFactory
from proxy.subscribable_reverse_proxy import SubscribableReverseProxy
from twisted.internet import reactor, protocol, task
from twisted.protocols import basic
from twisted.web import server
import config

def startPubSub(config):
    port = config["port"]
    expiredIn = config["expiredIn"]
    messageFormat = config["message_format"]
    waitFor = config["wait_for"]

    pubSubFactory = PubSubFactory(expiredIn, waitFor, messageFormat)
    reactor.listenTCP(port, pubSubFactory, config['backlog'])

    return pubSubFactory

def startReverseProxy(config, forwardRequest):
    proxiedHost = config["proxied_host"]
    port = config["port"]
    subscriptionPath = config["subscription_path"]

    proxy = SubscribableReverseProxy(proxiedHost[0], proxiedHost[1],
                             '', subscriptionPath);

    proxy.forwardRequest = forwardRequest
    site = server.Site(proxy)

    reactor.listenTCP(port, site, config['backlog'])

def profile(reporter, factory):
    print "calling", factory.pubsub.subscriber_size()
    basicFormatter = " :Memory Usage: %f, CPU Usage: %f\n"
    reporter.report(0,
                formatter = str(factory.pubsub.subscriber_size()) +\
                            basicFormatter)
def runProfiler(config, factory):
    if config["enabled"] != True:
        return

    reporter = config["reporter"](output = open(config["output"], "w"))
    interval = config["interval"]

    call_profile = lambda: profile(reporter, factory)
    task.LoopingCall(call_profile).start(interval, False)

def main():
    pubSubFactory = startPubSub(config.PUBLISH)
    startReverseProxy(config.REVERSE_PROXY, pubSubFactory.subscribe)
    runProfiler(config.PROFILE, pubSubFactory)

    reactor.run()

if __name__ == "__main__":
    main()


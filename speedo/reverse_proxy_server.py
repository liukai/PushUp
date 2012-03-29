from twisted.internet import reactor
from twisted.web import server
from reverse_proxy import LongPollingReverseProxyResource
import config

# TODO
#   * Add long polling expired time
#   * How to generalize this proxy?
#   * two threads are needed
#       - reverse proxy for clients
#       - receiving messages the proxied server
resource = LongPollingReverseProxyResource('127.0.0.1', 5000, '')
resource.longPollingPaths = config.LONG_POLLING_PATHS
site = server.Site(resource)
reactor.listenTCP(8080, site)
reactor.run()

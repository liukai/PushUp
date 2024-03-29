"""The application's Globals object"""

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from message_delivery import MessageDeliverer
from pylons import config
from profiler import *

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self, config):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        self.cache = CacheManager(**parse_cache_config_options(config))
        self.messageQueue = []
        self.userlist = {}

        self.channelId, self.messageDeliverer = self.startMessageDelivery(config)
        self.messageCounter = self.startProfiling(config)

    def startMessageDelivery(self, config):
        enabled = config.get("pubsub_server_enabled") == "true"
        channelId = 0
        messageDeliverer = None
        if enabled:
            host = config.get("pubsub_server_host")
            port = int(config["pubsub_server_port"])
            channelId = config["pubsub_server_channel"]

            messageDeliverer = MessageDeliverer(self.messageQueue, (host, port),
                                                channelId)
        return channelId, messageDeliverer

    def startProfiling(self, config):
        messageCounter = SafeCounter()
        if config.get("profile_enabled") != "true":
            return messageCounter

        interval = float(config.get("profile_interval"))
        output = open(config.get("profile_output"), "w")
        runReportUsage(interval, output, messageCounter)

        return messageCounter



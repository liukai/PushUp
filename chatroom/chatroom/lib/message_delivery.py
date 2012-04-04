import threading
import json
import socket
import time

class MessageDeliverer:
    """ This class will check the latest messages in the message queue
        and deliver them to a pub/sub server """
    def __init__(self, messageQueue, pubServerInfo, channelId):
        self.pos = 0
        self.messageQueue = messageQueue
        self.channelId = channelId + "\t"
        self.pubServerInfo = pubServerInfo
        self.socket = self._connectToServer(self.pubServerInfo)

    def notify(self):
        """ Check the new messages and deliver them to pub/sub server """
        size = len(self.messageQueue)
        for message in self.messageQueue[self.pos:size]:
            self._deliver(message)

        self.pos = size

    def close():
        self.socket.close()

    # --- Utilities ---
    def _deliver(self, message):
        jsonMessage = json.dumps(message)

        self.socket.send(self.channelId)
        self.socket.send(jsonMessage)
        self.socket.send("\r\n")

    def _connectToServer(self, serverInfo):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print serverInfo
        s.connect(serverInfo)
        return s

def _notifyForever(deliverer):
    """ This function set up a infinite loop to check
        new messages in a queue forever """
    while True:
        deliverer.notify()
        time.sleep(0) # yield

def runAutomaticMessageDelivery(messageQueue, pubServerInfo, channelId):
    """ This function setup a daemon thread to check the new messages """
    deliverer = MessageDeliverer(messageQueue, pubServerInfo, channelId)

    thread = threading.Thread(target = _notifyForever, args = (deliverer,))
    thread.daemon = True
    thread.start()


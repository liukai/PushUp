from datetime import datetime

class Message:
    def __init__(self, userId, content, time = datetime.now()):
        self.userId = userId
        self.content = content
        self.time = time
    def __str__(self):
        return "{'User Id': %s, 'Content': '%s', 'Time': %s}" % \
                (self.userId, self.content, self.time)

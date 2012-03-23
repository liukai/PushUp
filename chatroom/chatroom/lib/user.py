class User:
    def __init__(self, userId, name):
        self.userId = userId
        self.name = name
    def __str__(self):
        return "{'User Id': %s, 'Name': '%s'}" % \
                (self.userId, self.name)

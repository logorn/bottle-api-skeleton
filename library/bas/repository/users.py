
from apps.bootstrap import connection
from library.bas.entity.users import Users

class Users(object):
    """"""
    def __init__(self):
        connection.register([Users])
        self.collection = connection['mydatabase'].users

    def getCollection(self):
        return connection['mydatabase']
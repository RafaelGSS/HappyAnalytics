import MySQLdb
from env import *


class DB(object):
    def __init__(self):
        self.connected = False
        self.host = HOST
        self.user = USER
        self.password = PASSWORD
        self.database = DATABASE
        self.connection = None
        self.connect()

    def query(self, query):
        if not self.connected:
            return False

        self.connection.execute(query)
        return self.connection.fetchall()

    def select(self, table, columns="*", where=None, args=''):
        if not self.connected:
            return False
        
        qry = "SELECT {} FROM {} {}".format(columns, table, args)
        if where is not None:
            with_where = "SELECT {} FROM {} WHERE {}".format(columns, table, where)
            rows = self.connection.execute(with_where)
            if rows > 0:
                return self.connection.fetchall()
            return None

        rows = self.connection.execute(qry)
        if rows > 0:
            return self.connection.fetchall()
        return None

    def insert(self, table, columns, values):
        if not self.connected:
            return False

        qry = "INSERT INTO {}({}) VALUES({})".format(table, columns, values)
        self.connection.execute(qry)
        return True

    def insert_data(self, table, data):
        if not self.connected:
            return False

        keys = []
        values = []
        for k, v in data.items():
            keys.append(k)
            values.append(v)
        keys = ','.join(keys)
        values = '\'' + '\',\''.join(values) + '\''
        qry = "INSERT INTO {}({}) VALUES({})".format(table, keys, values)
        return self.connection.execute(qry)

    def update(self, table, where, set):
        if not self.connected:
            return False

        qry = "UPDATE {} SET {} WHERE {}".format(table, set, where)
        return self.connection.execute(qry)

    def connect(self):
        try:
            db = MySQLdb.connect(host=self.host,user=self.user, passwd=self.password, db=self.database)
            db.autocommit(True)
            self.connection = db.cursor(MySQLdb.cursors.DictCursor)
            self.connected = True
        except Exception:
            self.connected = False

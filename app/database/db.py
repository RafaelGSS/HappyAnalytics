import MySQLdb


class DB(object):
    def __init__(self):
        self.connected = False
        self.host = '127.0.0.1'
        self.user = 'root'
        self.password = 'toor'
        self.database = 'pylack'
        self.connection = None
        self.connect()

    def query(self, query):
        if not self.connected:
            return False

        self.connection.execute(query)
        return self.connection.fetchall()

    def select(self, table, columns="*"):
        if not self.connected:
            return False
        
        qry = "SELECT {} FROM {}".format(columns, table)
        self.connection.execute(qry)
        return self.connection.fetchall()

    def delete(self, table, where=None):
        if not self.connected:
            return False

        qry = "DELETE FROM {} {}".format(table, where if not where == None else "")
        self.connection.execute(qry)
        return self.connection.fetchall()

    def update(self, table, where):
        if not self.connected:
            return False
        
    def insert(self, table, columns, values):
        if not self.connected:
            return False

        qry = "INSERT INTO {}({}) VALUES({})".format(table, columns, values)
        self.connection.execute(qry)
        return True

    def insert_test(self, table, data):
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
        self.connection.execute("INSERT INTO messages(trigger_word,text,channel_id,user_id,token) VALUES('paulinho','paulinho: que isso ?','CAB2VSA7P','UAB2X1Z7F','6aEIbL0AaoylQbD9HNSlKYDR')")

        return True

    def connect(self):
        try:
            db = MySQLdb.connect(host=self.host,user=self.user, passwd=self.password, db=self.database)
            self.connection = db.cursor()
            self.connected = True
        except (Exception):
            self.connected = False
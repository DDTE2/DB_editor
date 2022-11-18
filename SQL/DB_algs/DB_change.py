from mysql import connector
from os.path import abspath
from json import loads

class change:
    def __init__(self, table):
        self.table = table

        path = abspath(__file__)[:-17] + 'user.data'
        with open(path, 'r') as file:
            data = loads(file.read())

        conn = connector.connect(host=data['host'],
                                 port=data['port'],
                                 user=data['user'],
                                 password=data['password'], database=data['database'])
        self.cursor = conn.cursor(buffered=True)

        self.add_requests = []
        self.del_requests = []

    def adds(self, row):
        self.add_requests.append(row)
    def dels(self, row):
        self.del_requests.append(row)

    def addr(self, column, data):
        request = 'INSERT INTO `' + self.table + '`'

        column = [f"`{c}`" for c in column]
        column = '('+ ', '.join(column) + ')'
        request += column

        request += 'VALUES'
        data = [f"`{c}`" for c in data]
        data = '(' + ', '.join(data) + ');'
        request += data

        self.cursor.execute(request)


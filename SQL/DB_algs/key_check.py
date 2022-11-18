from os.path import abspath
from json import loads
from mysql import connector

def check(name):
    path = abspath(__file__)[:-25] + '/user.data'
    with open(path, 'r') as file:
        data = loads(file.read())

    conn = connector.connect(host=data['host'],
                             port=data['port'],
                             user=data['user'],
                             password=data['password'], database=data['database'])
    if conn.is_connected():
        cursor = conn.cursor(buffered=True)
        cursor.execute(f'desc `{name}`;')
        row = cursor.fetchall()

        res = {c for c in range(len(row)) if row[c][3] != ''}

        return res
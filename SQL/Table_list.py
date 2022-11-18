from os.path import abspath
from json import loads
from mysql import connector

def creat_list():
    path = abspath(__file__)[:-17] + 'user.data'
    with open(path, 'r') as file:
        data = loads(file.read())

    conn = connector.connect(host=data['host'],
                             port=data['port'],
                             user=data['user'],
                             password=data['password'], database=data['database'])
    if conn.is_connected():
        cursor = conn.cursor(buffered=True)
        cursor.execute('SHOW TABLES;')
        row = cursor.fetchall()

        cursor.close()
        conn.close()

        res = [c[0] for c in row]
        return res

    return None
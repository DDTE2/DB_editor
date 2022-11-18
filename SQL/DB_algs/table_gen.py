from os.path import abspath
from json import loads
from mysql import connector

def table_gen(name):
    path = abspath(__file__)[:-24] + '/user.data'
    with open(path, 'r') as file:
        data = loads(file.read())

    conn = connector.connect(host=data['host'],
                             port=data['port'],
                             user=data['user'],
                             password=data['password'], database=data['database'])
    if conn.is_connected():
        try:
            cursor = conn.cursor(buffered=True)
            request = f'SHOW COLUMNS FROM {name};'
            #request = 'SELECT * FROM `pharmacy`.`goods`;'
            cursor.execute(request)
            columns = [c[0] for c in cursor.fetchall()]

            ############################################

            cursor = conn.cursor(buffered=True)
            #request = 'SHOW COLUMNS FROM goods;'
            request = f'SELECT * FROM `{name}`;'
            cursor.execute(request)
            table = cursor.fetchall()

            cursor.close()
            conn.close()

            print(table)

            return columns, table
        except Exception as error:
            return error
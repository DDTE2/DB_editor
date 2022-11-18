from os.path import abspath
from json import dumps, loads

class save:
        def __init__(self, host='127.0.0.1', port=3306,
        database='', user='', password=''):
                self.data = {'host': host,
                        'port': port,
                        'user': user,
                        'password': password,
                        'database': database}
                self.data_list()
        def data_list(self):
                path = abspath(__file__)[:-16] + 'data/host.data'

                with open(path, 'r') as file:
                        x = file.readlines()
                if not x:
                        with open(path, 'w') as file:
                                file.write(dumps(self.data))
                else:
                        f = False
                        res = set()
                        h = self.data['host']
                        print(set(x))
                        for c in set(x):
                                y = loads(c.replace('\n', ''))
                                if y['host'] == h:
                                        y['database'] += self.data['database']
                                        f = True
                                res.add(dumps(y))
                        if not f:
                                res.add(dumps(self.data))
                        *res, = res
                        res = '\n'.join(res)

                        with open(path, 'w') as file:
                                file.write(res)



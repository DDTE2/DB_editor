from mysql import connector

def connect(host='', port='',
         user='', password='', database=''):
    try:
        conn = connector.connect(host=host,
                         port=port,
                         user=user,
                         password=password, database=database)
        if conn.is_connected():
            cursor = conn.cursor(buffered=True)
            try:
                cursor.execute('SHOW DATABASES;')
                row = cursor.fetchall()

                cursor.close()
                conn.close()

                res = tuple(c[0] for c in row)
                return res
            except Exception as error:
                return error

    except Exception as error:
        print(error)
        error = error.args[0]
        try:
            match error:
                case 2005:
                    return 'Неправильный хост!'
                case 1045:
                    return 'Неверное имя или пароль!'
                case 1049:
                    return 'Неверное название базы данных!'
                case 2003:
                    return f'Не удалось подключится к серверу\n{host}:{port}'
                case _:
                    return 'При подключении к серверу \nпроизошла ошибка!'
            conn.close()
        except Exception as error:
            return str(error)
from json import  loads
try:
    with open('user.data', 'r') as file:
        data = loads(file.read())
    print(data)
    from Pages.py.Menu import Menu_Start
    Menu_Start()
except Exception as error:
    print(error)
    from Pages.py.First import First_Screen
    First_Screen()
from req import Api
from gui import Gui

def set_up():
    api = Api()
    users = api.get_users()
    #api.meeting_params()
    Gui(users, api)

if __name__ == '__main__':
    set_up()


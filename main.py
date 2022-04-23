from requests import Api
from gui import Gui

def set_up():
    """
    Initializes the API and then executes the command to collect all registered users
    These users are passed to the GUI constructor along with the API which holds important
    class parameters
    
    """
    api = Api()
    users = api.get_users()
    Gui(users, api)

if __name__ == '__main__':
    """
    Running set_up begins the program
    
    """
    set_up()


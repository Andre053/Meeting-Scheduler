from msal import ConfidentialClientApplication
import os # to get environment variables

class Service:
    """
    Service class initializes the connection to the daemon application 
    that interacts with Microsoft Graph API

    Requires credentials to be defined as global variables

    """
    
    def __init__(self):
        """
        Create environemnt variables for all Azure app credentials or fill them in manually

        Tenant ID: From Azure App
        Application ID: From Azure App
        Application Secret: Created through Azure, expires after a finite time
        User ID: The ID of a user with permissions within the application 
        
        """
        self.tenant_id = os.environ.get('TENANT_ID')
        self.app_id = os.environ.get('APP_ID') 
        self.secret = os.environ.get('APP_SECRET')
        self.user_id = os.environ.get('USER_ID')
        self.scopes = ['https://graph.microsoft.com/.default']        
        self.version = "v1.0"
        self.token = None
        self.app = None

        self.initialize() # initializes the service

    def initialize(self):
        """
        Get the authentication url and initialize the application 
        as a Confidential Client Application from MSAL

        Next we must obtain an authentication token which holds the
        permissions of the app, this token is saved as a parameter
        to be used in HTTP requests
        
        """

        auth_url = f'https://login.microsoftonline.com/{self.tenant_id}' # url to sign in

        self.app = ConfidentialClientApplication(self.app_id, authority=auth_url, client_credential=self.secret)
        self.token = self.get_token()

    def get_token(self):
        """
        Look for an authentication token within the cache of this machine
        If it cannot be found, aquire a new token and return it
        """
        result = None
        try: # check for old token to reuse
            result = self.app.acquire_token_silent(scopes=self.scopes, account=None)
        except:
            print("Could not find old token")
        if not result: # aquire a new token
            print("Aquiring a new token")
            result = self.app.acquire_token_for_client(scopes=self.scopes)
        if "access_token" in result:
            token = result['access_token'] # found the token
            print("New token created")
        else:
            token = None
            print("Error getting token")
            print(result)
        return token
from msal import ConfidentialClientApplication
import os # to get environment variables

class Service:
    def __init__(self):
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

        auth_url = f'https://login.microsoftonline.com/{self.tenant_id}' # url to sign in

        self.app = ConfidentialClientApplication(self.app_id, authority=auth_url, client_credential=self.secret)
        self.token = self.get_token()

    def get_token(self):
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
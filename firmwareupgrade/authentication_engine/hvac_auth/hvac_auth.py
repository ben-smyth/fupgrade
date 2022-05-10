from firmwareupgrade.authentication_engine.baseclass import BaseAuthentication
from config import settings
import hvac
import os

class HVACAuthentication(BaseAuthentication):
    def __init__(self):
        self.token = os.environ.get('HVAC_TOKEN')
        self.url = os.environ.get('HVAC_URL')
        self.device_info = settings['authentication-hvac']['device']


    def test_auth(self):
        hvac_client = hvac.Client(url = self.url,
                                  token = self.token)
        try:
            hvac_client.auth.token.renew_self(increment="700h")
            return True
        except Exception as e:
            print(f"Failed to connect to HVAC due to {e} \n\nPlease make sure you have configured necassary environment variables, and are able to reach the vault server")
            return False

    def get_device_creds(self):
        creds = {}
        creds['device'] = {}
        hvac_client = hvac.Client(self.url,
                                  self.token)
        hvac_creds = hvac_client.read(self.device_info['password_url'])
        creds['device']['username']=self.device_info['username']
        creds['device']['password']=hvac_creds['data']['value']
        return creds
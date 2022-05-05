from firmwareupgrade.authentication_engine.baseclass import BaseAuthentication
from config import settings
import hvac
import os

class HVACAuthentication(BaseAuthentication):
    def __init__(self):
        self.token = os.getenv('HVAC_TOKEN')
        self.url = os.getenv('HVAC_URL')
        self.device_info = settings['authentication-hvac']['device']


    def test_auth(self):
        hvac_client = hvac.Client(self.url,
                                  self.token)
        try:
            hvac_client.auth.token.renew_self(increment="700h")
            return True
        except Exception as e:
            print(e)
            return False,e

    def get_device_creds(self):
        creds = {}
        creds['device'] = {}
        hvac_client = hvac.Client(self.url,
                                  self.token)
        hvac_creds = hvac_client.read(self.device_info['password_url'])
        creds['device']['username']=self.device_info['username']
        creds['device']['password']=hvac_creds['data']['value']
        return creds
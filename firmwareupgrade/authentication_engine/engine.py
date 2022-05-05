from firmwareupgrade.authentication_engine.hvac_auth.hvac_auth import HVACAuthentication
from firmwareupgrade.authentication_engine.exceptions import AuthenticationError
from config import settings
import sys


def str_to_class(classname):
    """
    Given a class str-name, return it as an actual class, not a string.
    :param: classname
    :return: actual class
    """
    return getattr(sys.modules[__name__],classname)

class AuthenticationEngine:
    """
    Auth engine to handle authentication requirements
    """

    def __init__(self):
        self.engine = str_to_class(settings['settings']['authentication_engine'])()

    def test_auth(self):
        result = self.engine.test_auth()
        return result


    def get_device_creds(self):
        creds = self.engine.get_device_creds()
        return creds

    def get_scp_creds(self):
        creds = self.engine.get_scp_creds()
        return creds
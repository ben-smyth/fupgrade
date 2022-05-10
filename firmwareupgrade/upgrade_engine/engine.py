from firmwareupgrade.upgrade_engine.mrv.MRVEngine import MRVUpgrader
from firmwareupgrade.upgrade_engine.junos.JunOS import JunOSUpgrader
from firmwareupgrade.authentication_engine.engine import AuthenticationEngine

from config import settings
import sys


def str_to_class(classname):
    """
    Given a class str-name, return it as an actual class, not a string.
    :param: classname
    :return: actual class
    """
    return getattr(sys.modules[__name__],classname)


class UpgradeEngine:
    """
    engine class that handles the overall upgrade procedure. does not handle device specific logic.

    Integrates upgrade logic with NorNir logic

    Handles:
    - Providing correct credentials
    - Upgrade pathing
    - Pre and post upgrade checks
    """
    def __init__(
            self,
            task=None
    ):
        if task is not None:
            self.task = task
            self.hostname = self.task.host.hostname
            self.class_mapping = str_to_class(settings['upgrade-mappings'][self.task.host.dict()['groups'][0]])
            self.upgrade_path = self.task.host.extended_data()['upgrade_path']
            self.target_version = self.task.host.extended_data()['target_version']

    @property
    def credentials(self):
        creds={}
        creds['device'] = {}
        authengine = AuthenticationEngine()
        if self.task.host.username and self.task.host.password is not None:
            creds['device']['username'] = self.task.host.username
            creds['device']['password'] = self.task.host.password
        else:
            device_creds = authengine.get_device_creds()
            creds['device']['username'] = device_creds['device']['username']
            creds['device']['password'] = device_creds['device']['password']


        return creds

    def get_device_version(self):
        """
        given a task, get the devices hostname
        :return: dict: version : {'primary':str,'backup':'string'}
        """
        upgrade_class = self.class_mapping(self.hostname, self.credentials)
        version = upgrade_class.get_version()
        return version

    def pre_upgrade_checks(self):
        pass

    def upgrade(self):
        for i in self.upgrade_path:
            print(f"Upgrading {self.hostname} - Path: {i['upgrade']}/{len(self.upgrade_path)}")
            upgrade_class = self.class_mapping(self.hostname,self.credentials, firmware_path=i['firmware_location'], firmware_file_name=i['firmware_file_name'],target_version=self.target_version)
            upgrade_class.execute_upgrade()

    def post_upgrade_checks(self):
        pass


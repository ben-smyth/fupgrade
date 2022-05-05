from typing import Optional
import subprocess


class BaseDevice():
    """
    Base device for device specific upgrade logic to inherit from.
    """
    def __init__(
            self,
            hostname: str,
            creds: dict,
            firmware_path: str = None,
            firmware_file_name: str = None,
            target_version: dict = None
    ):
        self.hostname = hostname
        self.creds = creds
        self.firmware_path = firmware_path
        self.firmware_file_name = firmware_file_name
        self.firmware_full_path = f"{self.firmware_path}{self.firmware_file_name}"
        self.target_version = target_version

    def pingable(self) -> bool:
        """
        ping device and return true if its responding
        :return:
        """
        try:
            response = subprocess.check_output(f"ping -c 1 {self.hostname}", shell=True)
            return True
        except Exception:
            return False

    def get_version(self) -> dict:
        """
        Get device version
        :return: str device version
        """
        raise NotImplementedError

    def pre_upgrade_checks(self):
        """
        device specific pre upgrade checks
        """
        raise NotImplementedError

    def execute_upgrade(self):
        """
        Upgrade device using the provided firmware information
        """
        raise NotImplementedError

    def upload_file_to_device(self):
        """
        Method to put file on device but not upgrade
        """
        raise NotImplementedError

    def post_upgrade_checks(self):
        """
        device specific post upgrade checks
        """
        raise NotImplementedError
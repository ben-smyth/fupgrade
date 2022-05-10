import time

from firmwareupgrade.upgrade_engine.baseclass import BaseDevice
import firmwareupgrade.upgrade_engine.exceptions as upgrade_exceptions

from netmiko import ConnectHandler, SCPConn

import textfsm


class MRVUpgrader(BaseDevice):
    def _connect_to_device(self):
        device = {
            "device_type": "mrv_optiswitch",
            "host": self.hostname,
            "username": self.creds['device']['username'],
            "password": self.creds['device']['password'],
            "session_timeout": 600,
            "blocking_timeout": 1000,
            "fast_cli": False,
            "session_log": f"logs/shell_output/{self.hostname}.log",
            "session_log_file_mode": "append",
            "session_log_record_writes": True
        }

        self.connection = ConnectHandler(**device)

    def _get_interface(self):
        pass

    def _get_mac_address(self):
        pass

    def _get_lldp_neighbours(self):
        pass

    def get_version(self, already_connected=False):
        # create device connection
        if already_connected==False:
            self._connect_to_device()

        unparsed_versions = self.connection.send_command("show version backup")
        with open ('./firmwareupgrade/upgrade_engine/mrv/templates/show version backup') as template:
            fsm = textfsm.TextFSM(template)
            result = fsm.ParseTextToDicts(text=unparsed_versions)
        self.connection.disconnect()
        return result[0]

    def pre_upgrade_checks(self):
        # Get version
        # Ping
        # Get interfaces
            # Interface speeds
            # Errors
        # Get MAC addresses
        pass


    def execute_upgrade(self):
        def upgrade_logic(self,backup_upgrade=False):
            # create device connection
            self._connect_to_device()

            print(f"{self.hostname} - Writing to memory")
            self.connection.send_command(
                f"write mem")

            # SCP PUT
            print(f"{self.hostname} - Uploading SCP file")
            scp_channel = SCPConn(self.connection)
            scp_channel.establish_scp_conn()
            scp_channel.scp_put_file(self.firmware_full_path, f"/tmp/{self.firmware_file_name}")


            print(f"{self.hostname} - Installing firmware")
            self.connection.send_command(
                f"upgrade file {self.firmware_file_name}",
                expect_string="\(y\|n\)",
                delay_factor=6,
                max_loops=10000000,
                normalize=True,
                auto_find_prompt=False)

            if backup_upgrade == True:
                print(f"\n{self.hostname} - Install complete for backup partition")
                return

            else:
                # Reconnecting to ensure reboot command works properly
                self.connection.disconnect()
                time.sleep(5)
                self._connect_to_device()
                self.connection.send_command(
                    f"reboot",
                    expect_string="\(y\|n\)",
                    delay_factor=6,
                    max_loops=10000000,
                    normalize=True,
                    auto_find_prompt=False)
                time.sleep(5)
                reboot_timer_start=time.perf_counter()
                print(f"{self.hostname} - Initiating reboot")
                self.connection.send_command_timing('y')

                print(f"{self.hostname} - Waiting for reboot (waiting for max 10mins)")
                time.sleep(60)
                for i in range (1,10):
                    print(f"\n{self.hostname} - Trying to reach  following reboot...")
                    if self.pingable() == True:
                        print(f"{self.hostname} is back online. Time taken: {time.perf_counter()-reboot_timer_start}")
                        return True
                    else:
                        print(f"{self.hostname} has been offline for {i} minute(s)")
                        time.sleep(60)
                print(f"\n{self.hostname} has not come back online after 10 minutes. Marking as failed.")
                raise upgrade_exceptions.UpgradeError("Device did not come back online.")

        version = self.get_version()

        # Upgrade primary and backup partition
        if (str(version['primary']) != str(self.target_version)) and (
                str(version['backup']) != str(self.target_version)):
            print(f"{self.hostname} - Starting install 1 of 2 for Primary partion (reboot required)")
            upgrade_logic(self,False)
            print(f"{self.hostname} - 60 second grace period ")
            time.sleep(60)
            print(f"{self.hostname} - Starting install 2 of 2 for Backup partition (no reboot)")
            upgrade_logic(self,True)

        # Just upgrade primary
        elif (str(version['primary']) != str(self.target_version)) and (
                str(version['backup']) == str(self.target_version)):
            print(f"{self.hostname} - Starting install 1 of 1 for Primary partion (reboot required)")
            upgrade_logic(self,False)

        # Just upgrade backup partition
        elif (str(version['primary']) == str(self.target_version)) and (
                str(version['backup']) != str(self.target_version)):
            print(f"{self.hostname} - Starting install 1 of 1 for Backup partition (no reboot)")
            upgrade_logic(self,True)

        else:
            print(f"{self.hostname} - already on correct version...")

    def post_upgrade_checks(self):
        pass
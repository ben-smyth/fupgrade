# Sohonet Firmware Upgrader

The firmware upgrader is a pluggable software which deals with:

- Device inventory
- Pre/Post upgrade checks & snapshots
- Mapping devices to device specific upgrade logic
- Firmware locations
- Upgrade pathing
- Multithreading
- Logging


The software is designed to have **device specific** logic plugged into it in the form of the `baseclass`

##TODO
- [x] Authentication Engine for additional auth sources
- [ ] Improve logging
- [ ] Improve exception handling
- [ ] Notification Engine & Integration with Slack
- [ ] Scheduler - schedule jobs for later

## GLOBAL CONFIGURATION - `settings.toml`
The global config is kept inside `settings.toml`. This is where the upgrader can be customised for your requirements. 

Under `settings` inside the file, you can find the `notifications` and `authentication_engine`. This is where you can define which notification and authentication engines you wish to use.
You should use the direct class name for this to work properly.

Under `upgrade-mappings` you will see the mapping for  each device group (generally a device model), to its respective class, containing the device specific logic. You will only need to change this if you are extending the functionality of the upgrader.

## Managing the Inventory - `inventory/`
### HOSTS `inventory/hosts.yaml`
The inventory is managed by hierarchical files, somewhat similarly to Ansible. At the top is `inventory/hosts.yaml`

Below is all possible options available to the host and how that yaml file should be structured:
```commandline
---
host1:
  hostname: MR-OS904-I-1-LDP05-GB                                   # device hostname
  groups:
    - os904                                                         # device model
  username: admin                                                   # OPTIONAL device username
  password: xxxxxxx                                                 # OPTIONAL device password
    data:                                       
      target_version: '20_2_1'                                      # The version the firmware should be on
      upgrade_path:                                                 # The upgrade path for the firmware (if required)
        - upgrade: 1                                                # Number of upgrade, 1 being the first 
          firmware_location: 'firmware/mrv_scp/mrv/os-v/20.2.1/'    # Location of the firmware folder for this upgrade
          firmware_file_name: 'OS-V-20_2_1.17875.ver'               # Loation of the file for this upgrade
```
This example shows a host file with **ALL** information stored inside the host file. 
It is important to note that this is possible as it will allow multiple hosts to be upgrade to separate versions, follow separate upgrade paths, with different credentials. **However...**

### GROUPS `inventory/groups.yaml`

Most hosts will follow the same standard procedure with the same credentials. This is where `inventory/groups.yaml` comes in.

The host file will look like this in most cases:
```commandline
os904:
  data:
    target_version: '4_5_6'
    upgrade_path:
      - upgrade: 1
        firmware_location: 'firmware/mrv_scp/mrv/os9XX/4_5_6/OS90x/'
        firmware_file_name: 'os900-4_5_6.ver'
```
Key points for groups:
- Each host can be a member of **one** group only.
- Any data in `groups.yaml` will only be inherited if it is not present for the host in the `hosts.yaml` file.

## Running the Software - `upgrader-cli.py`
The upgrade can be initiated by running `upgrader-cli`. This will start by performing inventory checks and ask for confirmation before the upgrade kicks off.
Run `upgrader-cli --help` to see the options.

## Debugging
If the script fails or a device has not successfully upgraded, you should be informed via the output of the post upgrade checks.

When it fails, you can check `logs/` for output. This will show DEBUG level logs for important modules, and should give you tracebacks.

For upgrade logic that uses Netmiko, it will also be show in here. To find out which device the log belongs to you will need to associate the log with the thread number.


## Deployment
### Repo & Python installation
To deploy this software you will need to first clone the repo, and install all required python modules, as stated in `requirements.txt`

The recommended method for this is:
```commandline
pipenv install
pipenv shell
pip install -r requirements.txt
```
### Environement Variables
To run the upgrader using additional features, such as the authentication engine & notification engine, you will need to complete additional setup.
This will come in the form of environment variables, and/or additional config inside the `settings.toml` file.

To know which environment variables to add, go to each plugin. Each plugin will have a readme, containing the specifics for how to configure them.

### Inventory files
Complete the configuration of the inventory, using the guide above to help you.

### Firmware
Ensure the firmware is locally accessible, and readable by the python application.

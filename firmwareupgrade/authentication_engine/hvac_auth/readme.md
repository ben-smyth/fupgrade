# HVAC Setup

For HVAC to work please ensure the following env variables are configured:
```
HVAC_URL                - The URL (& port if non-standard) of the HVAC instance
HVAC_TOKEN              - The HVAC Token
```
## Config
You can add locations for HVAC credentials under `[authentication-hvac]` in the global config file.

To configure the device username and password, see the below exaple config:
```commandline
device = {'username'='upgrader_username', 'password_url'='secret/upgrader'}
scp = {'username'='scp','password_url'='secret/scp'}
```
## Token Management
Each time the software is used, the HVAC token for another 700H. If the HVAC token expires, you will need to generate a new one.
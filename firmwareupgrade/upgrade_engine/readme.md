# Upgrade Engine

The upgrade engine points upgrades towards the correct logic and handles upgrade pathing.

Inside `engine.py` you will find the class mappings.



In order to add your own device logic, create a folder for the manufacturer, and then create a class inside a new or existing python file.
This can then then inherit from `baseclass.py`
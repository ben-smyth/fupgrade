class UpgradeError(Exception):
    pass

class AuthenticationError(UpgradeError):
    pass
class BaseAuthentication:
    def test_auth(self) -> bool:
        """Test connection to credential server. Used in the initial checks before script is run"""
        raise NotImplementedError

    def get_device_creds(self) -> dict:
        """Get the device credentials required for the upgrade."""
        raise NotImplementedError

    def get_scp_creds(self) -> dict:
        """Get the scp credentials required for the upgrade."""
        raise NotImplementedError
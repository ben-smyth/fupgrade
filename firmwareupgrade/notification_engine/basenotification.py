class BaseNotification:
    def send_pre_notification(self):
        raise NotImplementedError

    def send_post_notification(self):
        raise NotImplementedError
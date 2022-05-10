
from kivy.uix.relativelayout import RelativeLayout
from datetime import datetime, timedelta
from kivy.properties import NumericProperty
from kivy.properties import StringProperty


class Notification(RelativeLayout):
    creation_date = NumericProperty()
    expire_date = NumericProperty()
    readable_creation_date = StringProperty()
    NOTIFICATION_EXPIRATION_TIME = 1  # in days

    def __init__(self, notification_info=None, **kwargs):
        super().__init__(**kwargs)
        creation_date = datetime.now()
        self.creation_date = creation_date.timestamp()
        expire_date = creation_date + timedelta(days=self.NOTIFICATION_EXPIRATION_TIME)
        self.expire_date = expire_date.timestamp()
        self.readable_creation_date = self.get_readable_creation_date()

    def get_readable_creation_date(self):
        return datetime.fromtimestamp(self.creation_date).strftime("%d-%m-%Y %H:%M:%S")

    def is_expired(self):
        return datetime.now().timestamp() > self.expire_date



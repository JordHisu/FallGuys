from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from datetime import datetime, timedelta
from kivy.properties import NumericProperty
from kivy.properties import StringProperty

Builder.load_file("props/notification_layout.kv")


class Notification(RelativeLayout):
    creation_date = NumericProperty()
    expire_date = NumericProperty()
    readable_creation_date = StringProperty()
    text = StringProperty()
    NOTIFICATION_EXPIRATION_TIME = 60  # in days

    def __init__(self, text, creation_date=None, expire_date=None, **kwargs):
        super().__init__(**kwargs)
        creation_date = datetime.now() if creation_date is None else datetime.fromtimestamp(creation_date)
        self.creation_date = creation_date.timestamp()

        if expire_date is None:
            expire_date = (creation_date + timedelta(seconds=self.NOTIFICATION_EXPIRATION_TIME)).timestamp()

        self.expire_date = expire_date
        self.readable_creation_date = self.get_readable_creation_date()
        self.text = text

    def get_readable_creation_date(self):
        return datetime.fromtimestamp(self.creation_date).strftime("%d-%m-%Y %H:%M:%S")

    def is_expired(self):
        return datetime.now().timestamp() > self.expire_date

    def get_json(self):
        return {
            'text': self.text,
            'creation_date': self.creation_date,
            'expire_date': self.expire_date,
        }

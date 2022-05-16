

from dataclasses import dataclass
from enum import Enum


class NotificationType(Enum):
    FALL = 'fall'
    STAND = 'stand'
    PANIC = 'panic'
    LYING = 'lying'


@dataclass
class NotificationData:
    data_type: str
    notification_type: NotificationType
    text: str

    def __post_init__(self):
        self.notification_type = NotificationType(self.notification_type)


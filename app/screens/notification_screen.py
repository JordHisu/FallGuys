
from kivy.lang import Builder
from kivy.properties import ListProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from props.notification import Notification
from utils.data.notification_data import NotificationData, NotificationType

Builder.load_file("screens/notification_screen_layout.kv")


class NotificationScreen(Screen):
    FETCH_NOTIFICATION_PERIOD = 10  # in seconds
    should_sort_notifications = BooleanProperty(False)
    stored_notifications = ListProperty()

    def on_stored_notifications(self, *args):
        self.update_notification_grid()

    def on_should_sort_notifications(self, *args):
        if self.should_sort_notifications:
            self.sort_notifications_by_creation_time()

    def update_notification_grid(self):
        new_notifications = self._get_stored_notifications()
        grid = self.ids.notification_grid
        for notification_info in new_notifications:
            notification = Notification(**notification_info)
            grid.add_widget(notification)
        self.clear_old_notifications()

    def sort_notifications_by_creation_time(self):
        grid = self.ids.notification_grid
        notifications = grid.children[:]
        grid.clear_widgets()
        notifications.sort(key=lambda x: x.creation_date)
        for notification in notifications:
            grid.add_widget(notification)
        self.should_sort_notifications = False

    def clear_old_notifications(self):
        grid = self.ids.notification_grid
        for notification in grid.children:
            if notification.is_expired():
                grid.remove_widget(notification)

    def _get_stored_notifications(self):
        notifications = self.stored_notifications
        self.stored_notifications = []
        return notifications

    def get_current_notifications_json(self):
        notification_widgets = self.ids.notification_grid.children
        return [notification.get_json() for notification in notification_widgets]

    def add_notification_from_json(self, notification_info):
        self.stored_notifications.append(notification_info)
        self.should_sort_notifications = True

    def add_notification(self, notification: NotificationData):
        if notification.notification_type not in (NotificationType.FALL, NotificationType.PANIC):
            return
        notification_info = {'text': notification.text}
        self.stored_notifications.append(notification_info)
        self.should_sort_notifications = True





from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from props.notification import Notification

Builder.load_file("screens/notification_screen_layout.kv")


class NotificationScreen(Screen):
    FETCH_NOTIFICATION_PERIOD = 10  # in seconds
    should_sort_notifications = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stored_notifications = []
        Clock.schedule_once(callback=self.update_notification_grid, timeout=0)
        Clock.schedule_interval(callback=self.update_notification_grid, timeout=self.FETCH_NOTIFICATION_PERIOD)

    def update_notification_grid(self, dt=None):
        new_notifications = self.fetch_notifications() + self._get_stored_notifications()
        grid = self.ids.notification_grid
        for notification_info in new_notifications:
            notification = Notification(**notification_info)
            grid.add_widget(notification)
        self.clear_old_notifications()

        if self.should_sort_notifications:
            self.sort_notifications_by_creation_time()

    def sort_notifications_by_creation_time(self):
        grid = self.ids.notification_grid
        notifications = grid.children[:]
        grid.clear_widgets()
        notifications.sort(key=lambda x: x.creation_date)
        for notification in notifications:
            grid.add_widget(notification)
        self.should_sort_notifications = False

    def fetch_notifications(self):
        handler = App.get_running_app().notification_handler
        return handler.get_notifications_from_server()

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

    def add_notification(self, notification_info):
        self.stored_notifications.append(notification_info)
        self.should_sort_notifications = True




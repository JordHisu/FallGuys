
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from props.notification import Notification

Builder.load_file("screens/notification_screen_layout.kv")


class NotificationScreen(Screen):
    FETCH_NOTIFICATION_PERIOD = 10  # in seconds

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(callback=self.update_notification_grid, timeout=self.FETCH_NOTIFICATION_PERIOD)

    def update_notification_grid(self, dt=None):
        new_notifications = self.fetch_notifications()
        grid = self.ids.notification_grid
        for notification_info in new_notifications:
            notification = Notification(notification_info)
            grid.add_widget(notification)
        self.clear_old_notifications()

    def fetch_notifications(self):
        handler = App.get_running_app().notification_handler
        return handler.get_notifications_from_server()

    def clear_old_notifications(self):
        grid = self.ids.notification_grid
        for notification in grid.children:
            if notification.is_expired():
                grid.remove_widget(notification)

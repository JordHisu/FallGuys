import os
from glob import glob

import kivy.utils
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager


from kivy.uix.relativelayout import RelativeLayout
from datetime import datetime, timedelta
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen


class NotificationHandler:
    def get_notifications_from_server(self):
        return [
            {
                'type': 'X',
                'time': '23:59'
            }
        ]


class FallGuysApp(App):
    MAIN_LAYOUT_FILE = 'layout.kv'
    notification_handler = NotificationHandler()

    def build(self):
        root = self.load_kv_files()
        return root

    def load_kv_files(self):
        return Builder.load_string(KV)


class TopOfEverything(FloatLayout):
    INITIAL_WINDOW_SIZE = [300, 533]

    def __init__(self, **kwargs):
        super(TopOfEverything, self).__init__(**kwargs)
        self.decide_screen_size()
        self.screen_manager = None

    def decide_screen_size(self):
        platform = kivy.utils.platform
        if platform == 'win':
            Window.size = self.INITIAL_WINDOW_SIZE


class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.after_init, 0)

    def after_init(self, dt):
        App.get_running_app().root.screen_manager = self

    def change_screen(self, screen_name, *args):
        self.current = screen_name


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


class NotificationScreen(Screen):
    FETCH_NOTIFICATION_PERIOD = 3  # in seconds

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




KV = """
TopOfEverything:
    MyScreenManager:
        NotificationScreen:
        
<Notification>:
    canvas:
        Color:
            rgba: .5, .5, .5, 1
        Line:
            rectangle: (0, 0, self.width, self.height)
    size_hint_y: None
    height: dp(80)
    Label:
        pos_hint: {'x': .02, 'top': .95}
        size_hint: None, None
        size: self.texture_size
        font_size: dp(12)
        text: root.readable_creation_date
        color: .5, .5, .5, 1
    Label:
        pos_hint: {'center_x': .5, 'center_y': .5}
        size_hint: None, None
        size: self.texture_size
        font_size: dp(17)
        text: "O usuário caiu!"
        
<NotificationScreen>:
    name: "NotificationScreen"
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "Notifications"
            font_size: dp(30)
            size_hint_y: None
            height: dp(self.texture_size[1] + 30)
        ScrollView:
            canvas:
                Color:
                    rgba: .8, .2, .2, 1
                Line:
                    rectangle: (self.x, self.y, self.width, self.height)
            GridLayout:
                id: notification_grid
                cols: 1
                height: self.minimum_height
                size_hint_y: None
                orientation: 'lr-bt'
                canvas:
                    Color:
                        rgba: .5, .8, .2, .2
                    Rectangle:
                        pos: self.pos
                        size: self.size
        BoxLayout:
            size_hint_y: None
            height: root.height * .09
"""


if __name__ == '__main__':
    FallGuysApp().run()

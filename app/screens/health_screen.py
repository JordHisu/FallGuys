
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import Screen
from utils.data.notification_data import NotificationData, NotificationType

Builder.load_file("screens/health_screen_layout.kv")


class HealthScreen(Screen):
    person_fell = BooleanProperty(False)
    person_lying = BooleanProperty(False)

    def add_barometer_point(self, barometer_data):
        self.ids.barometer_graph.add_value(barometer_data.source, barometer_data.value)

    def add_step_point(self, step_data):
        self.ids.step_graph.add_value(step_data.value)

    def receive_notification(self, notification: NotificationData):
        if notification.notification_type == NotificationType.FALL:
            self.fall_trigger()
            return
        if notification.notification_type == NotificationType.LYING:
            self.lying_trigger()
            return
        if notification.notification_type == NotificationType.STAND:
            self.stand_trigger()
            return

    def fall_trigger(self):
        self.person_fell = True
        self.person_lying = False
        self.ids.person.angle = 90

    def lying_trigger(self):
        self.person_fell = False
        self.person_lying = True
        self.ids.person.angle = 270

    def stand_trigger(self):
        self.person_fell = False
        self.person_lying = False
        self.ids.person.angle = 0



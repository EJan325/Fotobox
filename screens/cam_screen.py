from widgets.rounded_button import RoundedButton
from widgets.camera_widget import CameraWidget

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.clock import Clock

from config import TEMP_FILE

class PhotoBoothScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.countdown_seconds = 3
        self.countdown_remaining = 0
        self.countdown_event = None

        self.camera = CameraWidget(allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.camera)

        # Countdown Label
        self.countdown_label = Label(text='', font_size=150,
                                     color=(1, 1, 1, 1),
                                     pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.layout.add_widget(self.countdown_label)

        self.btn_photo = RoundedButton(
            text="Foto",
            font_size=32,
            size_hint=(0.25, 0.15),
            pos_hint={'right': 0.95, 'y': 0.05},
            background_color=(0, 0, 0, 0.5)
        )
        self.btn_photo.bind(on_release=self.start_countdown)
        self.layout.add_widget(self.btn_photo)

        self.btn_gallery = RoundedButton(
            text="Galerie",
            font_size=32,
            size_hint=(0.25, 0.15),
            pos_hint={'x': 0.05, 'top': 0.95},
            background_color=(0, 0, 0, 0.5)
        )
        self.btn_gallery.bind(on_release=self.go_to_gallery)
        self.layout.add_widget(self.btn_gallery)

        self.add_widget(self.layout)

    def go_to_gallery(self, *args):
        self.manager.current = "gallery"

    def start_countdown(self, instance):
        if self.countdown_event:
            return  # Countdown läuft schon
        self.countdown_remaining = self.countdown_seconds
        self.countdown_label.text = str(self.countdown_remaining)
        self.btn_photo.disabled = True
        self.btn_gallery.disabled = True
        self.countdown_event = Clock.schedule_interval(self._countdown_step, 1)

    def _countdown_step(self, dt):
        self.countdown_remaining -= 1
        if self.countdown_remaining > 0:
            self.countdown_label.text = str(self.countdown_remaining)
        else:
            Clock.unschedule(self.countdown_event)
            self.countdown_event = None
            self.countdown_label.text = ''
            self.take_photo()

    def take_photo(self):
        # Foto nur in TEMP_FILE speichern
        self.camera.capture(TEMP_FILE)
        image_view = self.manager.get_screen("imageview")
        image_view.set_image(TEMP_FILE, temp=True)
        self.manager.current = "imageview"
        self.btn_photo.disabled = False
        self.btn_gallery.disabled = False
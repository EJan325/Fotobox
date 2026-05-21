from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

from picamera2 import Picamera2

import time


class CameraWidget(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.picam2 = Picamera2()

        preview_config = self.picam2.create_preview_configuration(
            main={"format": "RGB888", "size": (2304, 1296)}
        )

        self.picam2.configure(preview_config)

        self.picam2.start()

        time.sleep(0.1)

        self.update_event = Clock.schedule_interval(
            self.update,
            1 / 25.0
        )

    def update(self, dt):
        try:
            frame = self.picam2.capture_array()

            buf = frame.tobytes()

            h, w = frame.shape[:2]

            if not self.texture:
                self.texture = Texture.create(
                    size=(w, h),
                    colorfmt='rgb'
                )

                self.texture.flip_vertical()
                self.texture.flip_horizontal()

            self.texture.blit_buffer(
                buf,
                colorfmt='bgr',
                bufferfmt='ubyte'
            )

            self.canvas.ask_update()

        except Exception as e:
            print(e)

    def capture(self, path):
        self.picam2.capture_file(path)
from kivy.uix.image import AsyncImage


class ClickableImage(AsyncImage):

    def __init__(self, image_path, gallery_screen, **kwargs):
        super().__init__(**kwargs)

        self.image_path = image_path
        self.gallery_screen = gallery_screen

        self.touch_start_pos = None

    def on_touch_down(self, touch):

        if self.collide_point(*touch.pos):
            self.touch_start_pos = touch.pos
            return False

        return super().on_touch_down(touch)

    def on_touch_up(self, touch):

        if self.collide_point(*touch.pos) and self.touch_start_pos:

            start_x, start_y = self.touch_start_pos
            end_x, end_y = touch.pos

            distance = (
                (end_x - start_x) ** 2 +
                (end_y - start_y) ** 2
            ) ** 0.5

            if distance < 20:
                self.gallery_screen.open_image(
                    self.image_path
                )

            self.touch_start_pos = None

            return True

        return super().on_touch_up(touch)
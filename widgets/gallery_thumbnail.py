from kivy.metrics import dp
from kivy.uix.image import AsyncImage
from kivy.properties import StringProperty, ObjectProperty


class GalleryThumbnail(AsyncImage):
    image_path = StringProperty("")
    gallery_view = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allow_stretch = True
        self.keep_ratio = True
        self.size_hint_x = 1
        self.size_hint_y = None
        self.height = dp(200)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.ud['gallery_thumb_start'] = touch.pos
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        start_pos = touch.ud.get('gallery_thumb_start')
        if start_pos and self.collide_point(*touch.pos):
            dx = abs(touch.x - start_pos[0])
            dy = abs(touch.y - start_pos[1])
            if dx < dp(15) and dy < dp(15):
                if self.gallery_view:
                    self.gallery_view.open_image(self.image_path)
        return super().on_touch_up(touch)

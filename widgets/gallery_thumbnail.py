from kivy.metrics import dp
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.image import AsyncImage
from kivy.properties import StringProperty, ObjectProperty


class GalleryThumbnail(ButtonBehavior, AsyncImage):
    image_path = StringProperty("")
    gallery_view = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allow_stretch = True
        self.keep_ratio = True
        self.size_hint_x = 1
        self.size_hint_y = None
        self.height = dp(200)

    def on_release(self):
        if self.gallery_view:
            self.gallery_view.open_image(self.image_path)

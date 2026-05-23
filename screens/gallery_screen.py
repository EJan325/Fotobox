from widgets.rounded_button import RoundedButton
from widgets.gallery_thumbnail import GalleryThumbnail

from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivy.uix.recycleview import RecycleView
from kivy.graphics import Color, Rectangle

from config import BILDER_DIR

import os

KV = '''
#:import dp kivy.metrics.dp

<GalleryRecycleView>:
    viewclass: 'GalleryThumbnail'
    do_scroll_x: False
    do_scroll_y: True
    scroll_type: ['bars', 'content']

    RecycleGridLayout:
        cols: 3
        default_size: None, dp(200)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        spacing: dp(10)
        padding: dp(10)
'''

Builder.load_string(KV)


class GalleryRecycleView(RecycleView):

    THUMB_SIZE = (200, 200)

    def __init__(self, gallery_screen, **kwargs):
        super().__init__(**kwargs)

        self.gallery_screen = gallery_screen
        self.viewclass = "GalleryThumbnail"
        self.image_paths = []
        self.scroll_type = ['bars', 'content']
        self.do_scroll_x = False
        self.do_scroll_y = True
        self.bar_width = dp(10)
        self.thumbnail_dir = os.path.join(BILDER_DIR, ".thumbs")
        os.makedirs(self.thumbnail_dir, exist_ok=True)

    def _ensure_thumbnail(self, img_path):
        thumb_name = os.path.basename(img_path)
        thumb_path = os.path.join(self.thumbnail_dir, thumb_name)

        if os.path.exists(thumb_path) and os.path.getmtime(thumb_path) >= os.path.getmtime(img_path):
            return thumb_path

        try:
            from PIL import Image as PILImage
        except ImportError:
            return img_path

        try:
            with PILImage.open(img_path) as image:
                source_mode = image.mode
                target_size = self.THUMB_SIZE
                resample = getattr(PILImage, 'Resampling', PILImage).LANCZOS
                image.thumbnail(target_size, resample)

                if source_mode in ('RGBA', 'LA') or (source_mode == 'P' and image.info.get('transparency')):
                    image.save(thumb_path, format='PNG')
                else:
                    image = image.convert('RGB')
                    image.save(thumb_path, format='JPEG', quality=70)
        except Exception:
            return img_path

        return thumb_path

    def load_images(self):
        self.image_paths = []
        rv_data = []

        if os.path.exists(BILDER_DIR):
            for file in sorted(os.listdir(BILDER_DIR), reverse=True):
                if file.lower().endswith((".png", ".jpg", ".jpeg")):
                    img_path = os.path.join(BILDER_DIR, file)
                    self.image_paths.append(img_path)
                    thumb_source = self._ensure_thumbnail(img_path)
                    rv_data.append({
                        "source": thumb_source,
                        "image_path": img_path,
                        "gallery_view": self,
                    })

        self.data = rv_data

    def open_image(self, path):
        try:
            index = self.image_paths.index(path)
        except ValueError:
            index = 0

        image_view = self.gallery_screen.manager.get_screen("imageview")
        image_view.set_image(
            path,
            temp=False,
            from_gallery=True,
            gallery_images=self.image_paths,
            image_index=index
        )
        self.gallery_screen.manager.current = "imageview"


class GalleryScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self._update_bg, size=self._update_bg)

        root = FloatLayout()

        self.gallery_view = GalleryRecycleView(self, size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        root.add_widget(self.gallery_view)

        back_button = RoundedButton(
            text="Zurück",
            font_size=32,
            size_hint=(0.25, 0.15),
            pos_hint={'x': 0.05, 'top': 0.95},
            background_color=(0, 0, 0, 0.5)
        )
        back_button.bind(on_press=self.go_back)
        root.add_widget(back_button)

        self.add_widget(root)

    def on_enter(self):
        self.gallery_view.load_images()

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def go_back(self, instance):
        self.manager.current = "photo"


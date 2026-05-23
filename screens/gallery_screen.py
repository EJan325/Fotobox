from widgets.rounded_button import RoundedButton
from widgets.gallery_thumbnail import GalleryThumbnail

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivy.uix.recycleview import RecycleView

from config import BILDER_DIR

import os

KV = '''
#:import dp kivy.metrics.dp

<GalleryRecycleView>:
    viewclass: 'GalleryThumbnail'

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

    def __init__(self, gallery_screen, **kwargs):
        super().__init__(**kwargs)

        self.gallery_screen = gallery_screen
        self.viewclass = "GalleryThumbnail"
        self.image_paths = []
        self.scroll_type = ['bars']
        self.bar_width = dp(10)

    def load_images(self):
        self.image_paths = []
        rv_data = []

        if os.path.exists(BILDER_DIR):
            for file in sorted(os.listdir(BILDER_DIR), reverse=True):
                if file.lower().endswith((".png", ".jpg", ".jpeg")):
                    img_path = os.path.join(BILDER_DIR, file)
                    self.image_paths.append(img_path)
                    rv_data.append({
                        "source": img_path,
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

        main_layout = BoxLayout(orientation="vertical", spacing=0, padding=0)

        self.gallery_view = GalleryRecycleView(self, size_hint=(1, 0.85))
        main_layout.add_widget(self.gallery_view)

        back_button = RoundedButton(
            text="Zurück",
            size_hint=(1, 0.15)
        )
        back_button.bind(on_press=self.go_back)
        main_layout.add_widget(back_button)

        self.add_widget(main_layout)

    def on_enter(self):
        self.gallery_view.load_images()

    def go_back(self, instance):
        self.manager.current = "photo"
from widgets.rounded_button import RoundedButton
from widgets.clickable_image import ClickableImage

from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen

from config import BILDER_DIR
import os


class GalleryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        # Hintergrundfarbe für die Gallery hinzufügen
        from kivy.graphics import Color, Rectangle
        with layout.canvas.before:
            Color(0.65, 0.55, 0.4, 1)  # Warmes Eichenholz-Hellbraun
            self.bg_rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_bg, pos=self._update_bg)

        scroll = ScrollView(size_hint=(1, 0.9), pos_hint={'x': 0, 'y': 0})
        self.grid = GridLayout(cols=3, spacing=10, size_hint_y=None, padding=10)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        scroll.add_widget(self.grid)

        btn_back = RoundedButton(
            text="Zurück",
            font_size=28,
            size_hint=(0.2, 0.1),
            pos_hint={'x': 0.02, 'top': 0.98},
            background_color=(0, 0, 0, 0.5)
        )
        btn_back.bind(on_release=self.go_back)

        layout.add_widget(scroll)
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def go_back(self, *args):
        self.manager.current = "photo"

    def _update_bg(self, instance, value):
        """Hintergrund an Layout-Größe anpassen"""
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def on_pre_enter(self, *args):
        self.load_images()

    def load_images(self):
        self.grid.clear_widgets()
        self.image_paths = []  # Liste aller Bildpfade für Swipe-Navigation
        
        if os.path.exists(BILDER_DIR):
            # Sammle alle Bildpfade
            for file in sorted(os.listdir(BILDER_DIR), reverse=True):
                if file.lower().endswith((".png", ".jpg", ".jpeg")):
                    img_path = os.path.join(BILDER_DIR, file)
                    self.image_paths.append(img_path)
            
            # Erstelle Thumbnails
            for img_path in self.image_paths:
                thumb = ClickableImage(
                    source=img_path,
                    size_hint_y=None, 
                    height=200, 
                    allow_stretch=True,
                    image_path=img_path,
                    gallery_screen=self
                )
                self.grid.add_widget(thumb)

    def open_image(self, path):
        """Öffnet ein Bild - wird nur bei tatsächlichen Klicks aufgerufen"""
        # Finde Index des aktuellen Bildes für Swipe-Navigation
        try:
            image_index = self.image_paths.index(path)
        except ValueError:
            image_index = 0
            
        image_view = self.manager.get_screen("imageview")
        image_view.set_image(
            path, 
            temp=False, 
            from_gallery=True,
            gallery_images=self.image_paths,
            image_index=image_index
        )
        self.manager.current = "imageview"
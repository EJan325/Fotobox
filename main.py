from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.factory import Factory

from screens.cam_screen import PhotoBoothScreen
from screens.image_screen import ImageViewScreen
from screens.gallery_screen import GalleryScreen
from widgets.gallery_thumbnail import GalleryThumbnail

# Registriere GalleryThumbnail in der Factory
Factory.register("GalleryThumbnail", cls=GalleryThumbnail)


class PhotoBoothApp(App):

    def build(self):

        Window.fullscreen = 'auto'

        sm = ScreenManager()

        sm.add_widget(
            PhotoBoothScreen(name="photo")
        )

        sm.add_widget(
            ImageViewScreen(name="imageview")
        )

        sm.add_widget(
            GalleryScreen(name="gallery")
        )

        return sm


PhotoBoothApp().run()
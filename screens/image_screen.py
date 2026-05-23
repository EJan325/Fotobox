from widgets.rounded_button import RoundedButton

from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout

import os, time, shutil

from config import BILDER_DIR

class ImageViewScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.image_widget = Image(allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.image_widget)

        self.btn_save = RoundedButton(
            text="Speichern",
            font_size=32,
            size_hint=(0.25, 0.15),
            pos_hint={'right': 0.95, 'y': 0.05},
            background_color=(0, 0, 0, 0.5)
        )
        self.btn_save.bind(on_release=self.save_photo)
        # Test-Event zusätzlich binden
        self.btn_save.bind(on_press=lambda x: print("Speichern/Zurück-Button gedrückt"))
        self.layout.add_widget(self.btn_save)
        print("Speichern/Zurück-Button erstellt und gebunden")

        self.btn_delete = RoundedButton(
            text="Löschen",
            font_size=32,
            size_hint=(0.3, 0.15),
            pos_hint={'x': 0.05, 'y': 0.05},
            background_color=(0, 0, 0, 0.5)
        )
        self.btn_delete.bind(on_release=self.delete_photo)
        # Test-Event zusätzlich binden
        self.btn_delete.bind(on_press=lambda x: print("Löschen-Button gedrückt"))
        self.layout.add_widget(self.btn_delete)
        print("Löschen-Button erstellt und gebunden")

        self.add_widget(self.layout)

        self.current_path = None
        self.temp = False
        self.from_gallery = False
        self.gallery_images = []  # Liste aller Gallery-Bilder
        self.current_image_index = 0  # Index des aktuellen Bildes
        
        # Swipe-Erkennung
        self.touch_start_x = None
        self.min_swipe_distance = 10  # Mindestdistanz für Swipe

    def set_image(self, path, temp=False, from_gallery=False, gallery_images=None, image_index=0):
        print(f"set_image aufgerufen - from_gallery: {from_gallery}, path: {path}")
        
        self.image_widget.source = path
        self.image_widget.reload()
        self.current_path = path
        self.temp = temp
        self.from_gallery = from_gallery
        
        # Gallery-Navigation Setup
        if from_gallery and gallery_images:
            self.gallery_images = gallery_images
            self.current_image_index = image_index
            print(f"Gallery-Modus: {len(gallery_images)} Bilder, Index: {image_index}")
        else:
            self.gallery_images = []
            self.current_image_index = 0
            print("Foto-Modus")
        
        # Button-Text je nach Herkunft anpassen
        if from_gallery:
            # Aus Gallery: Zurück-Button statt Speichern
            self.btn_save.text = "Zurück"
            self.btn_delete.text = "Löschen"
            print("Buttons auf 'Zurück' und 'Löschen' gesetzt")
        else:
            # Neues Foto: Speichern und Löschen
            self.btn_save.text = "Speichern"
            self.btn_delete.text = "Löschen"
            print("Buttons auf 'Speichern' und 'Löschen' gesetzt")

    def save_photo(self, instance):
        print(f"save_photo aufgerufen - from_gallery: {self.from_gallery}, Button-Text: {self.btn_save.text}")
        
        if self.from_gallery:
            # Zurück zur Gallery
            print("Gehe zurück zur Gallery")
            self.manager.current = "gallery"
        else:
            # Foto speichern (nur bei neuen Fotos)
            print("Speichere neues Foto")
            if self.temp and os.path.exists(self.current_path):
                os.makedirs(BILDER_DIR, exist_ok=True)
                filename = os.path.join(
                    BILDER_DIR,
                    time.strftime("photo_%Y%m%d_%H%M%S.jpg")
                )
                shutil.move(self.current_path, filename)
            self.manager.current = "photo"

    def delete_photo(self, instance):
        print(f"delete_photo aufgerufen - from_gallery: {self.from_gallery}, Pfad: {self.current_path}")
        
        if os.path.exists(self.current_path):
            os.remove(self.current_path)
            print(f"Datei gelöscht: {self.current_path}")
        else:
            print(f"Datei existiert nicht: {self.current_path}")
        
        # Zurück zur Herkunft: Gallery oder Kamera
        if self.from_gallery:
            print("Gehe zurück zur Gallery nach Löschen")
            self.manager.current = "gallery"
        else:
            print("Gehe zurück zur Kamera nach Löschen")
            self.manager.current = "photo"

    def on_touch_down(self, touch):
        # Prüfe nur die spezifischen Buttons (nicht alle Widgets)
        if (self.btn_save.collide_point(*touch.pos) or 
            self.btn_delete.collide_point(*touch.pos)):
            print(f"Touch auf Button erkannt")
            return super().on_touch_down(touch)
        
        # Swipe-Handling für Gallery-Modus
        if self.from_gallery and self.gallery_images:
            self.touch_start_x = touch.x
            print(f"Swipe-Start erkannt bei x={touch.x}")
            return True
        
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        # Prüfe nur die spezifischen Buttons (nicht alle Widgets)
        if (self.btn_save.collide_point(*touch.pos) or 
            self.btn_delete.collide_point(*touch.pos)):
            print(f"Touch-Release auf Button")
            return super().on_touch_up(touch)
        
        # Swipe-Handling für Gallery-Modus
        if (self.from_gallery and self.gallery_images and 
            self.touch_start_x is not None):
            
            # Berechne Swipe-Distanz
            swipe_distance = touch.x - self.touch_start_x
            print(f"Swipe-Distanz: {swipe_distance} (Start: {self.touch_start_x}, Ende: {touch.x})")
            
            if abs(swipe_distance) > self.min_swipe_distance:
                if swipe_distance > 0:
                    # Swipe nach rechts = vorheriges Bild
                    print("Swipe rechts - vorheriges Bild")
                    self.show_previous_image()
                else:
                    # Swipe nach links = nächstes Bild
                    print("Swipe links - nächstes Bild")
                    self.show_next_image()
            else:
                print(f"Swipe zu kurz: {abs(swipe_distance)} < {self.min_swipe_distance}")
            
            self.touch_start_x = None
            return True
        
        return super().on_touch_up(touch)

    def show_next_image(self):
        """Zeige nächstes Bild in der Gallery"""
        if self.current_image_index < len(self.gallery_images) - 1:
            self.current_image_index += 1
            new_path = self.gallery_images[self.current_image_index]
            self.current_path = new_path
            self.image_widget.source = new_path
            self.image_widget.reload()
            # Stelle sicher, dass Buttons korrekt bleiben
            self._update_button_texts()

    def show_previous_image(self):
        """Zeige vorheriges Bild in der Gallery"""
        if self.current_image_index > 0:
            self.current_image_index -= 1
            new_path = self.gallery_images[self.current_image_index]
            self.current_path = new_path
            self.image_widget.source = new_path
            self.image_widget.reload()
            # Stelle sicher, dass Buttons korrekt bleiben
            self._update_button_texts()

    def _update_button_texts(self):
        """Aktualisiert Button-Texte basierend auf Herkunft"""
        print(f"_update_button_texts - from_gallery: {self.from_gallery}")
        if self.from_gallery:
            self.btn_save.text = "Zurück"
            self.btn_delete.text = "Löschen"
            print("Buttons auf Gallery-Modus gesetzt")
        else:
            self.btn_save.text = "Speichern"
            self.btn_delete.text = "Löschen"
            print("Buttons auf Foto-Modus gesetzt")
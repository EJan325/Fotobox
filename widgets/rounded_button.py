from kivy.uix.button import Button


class RoundedButton(Button):
    def __init__(self, **kwargs):
        self.custom_bg_color = kwargs.get(
            'background_color',
            (0, 0, 0, 0.5)
        )

        kwargs['background_color'] = (0, 0, 0, 0)

        super().__init__(**kwargs)

        self.background_normal = ''
        self.background_down = ''
        self.background_disabled_normal = ''

        with self.canvas.before:
            from kivy.graphics import Color, RoundedRectangle

            self.bg_color = Color(*self.custom_bg_color)

            self.bg_rect = RoundedRectangle(
                size=self.size,
                pos=self.pos,
                radius=[15]
            )

        self.bind(size=self._update_bg, pos=self._update_bg)

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
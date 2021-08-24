from kivymd.app import MDApp
from mainwidget import MainWidget
from kivymd.uix.snackbar import Snackbar
from kivy.lang.builder import Builder
from popups import ModbusPopup

class MainApp(MDApp):
    """
    Classe com o aplicativo
    """
    def build(self):
        """
        Método que gera o aplicativo com base no Widget principal
        :return: Aplicativo
        """
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.primary_hue = '500'
        self.theme_cls.accent_pallete = "Gray"
        self._widget = MainWidget(vel_ramp=1000,server_ip='127.0.0.1',server_port=502)
        return self._widget







if __name__ == '__main__':
    Builder.load_string(open('mainwidget.kv',encoding='utf-8').read(),rulesonly=True)
    Builder.load_string(open('popups.kv', encoding='utf-8').read(), rulesonly=True)
    MainApp().run()
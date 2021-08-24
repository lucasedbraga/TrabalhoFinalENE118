from kivymd.app import MDApp
from mainwidget import MainWidget
from kivymd.uix.snackbar import Snackbar
from kivy.lang.builder import Builder

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
        self._widget = MainWidget()
        return self._widget

    def clock_button(self, button):
        Snackbar(text='Teste1').open()

    def menu_button(self, button):
        Snackbar(text='Teste2').open()





if __name__ == '__main__':
    Builder.load_string(open('mainwidget.kv',encoding='utf-8').read(),rulesonly=True)
    MainApp().run()
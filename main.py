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
        self._widget = MainWidget(vel_ramp=1000,server_ip='127.0.0.1',server_port=502,
                                  modbus_addrs = {
                                      't_part':798,
                                      'freq_des':799,
                                      'freq_mot':800,
                                      'tensao':801,
                                      'bt_Desliga/Liga': 802,
                                      'rotacao':803,
                                      'pot_entrada':804,
                                      'corrente':805,
                                      'temp_estator':806,
                                      'vel_esteira':807,
                                      'carga':808,
                                      'peso_obj':809,
                                      'cor_obj_R':810,
                                      'cor_obj_G':811,
                                      'cor_obj_B':812,
                                      'numObj_est_1':813,
                                      'numObj_est_2':814,
                                      'numObj_est_3':815,
                                      'numObj_est_nc':816,
                                      'filtro_est_1':901,
                                      'filtro_est_2':902,
                                      'filtro_est_3':903,
                                      'filtro_cor_r_1':1001,
                                      'filtro_cor_g_1':1002,
                                      'filtro_cor_b_1':1003,
                                      'filtro_massa_1':1004,
                                      'filtro_cor_r_2':1011,
                                      'filtro_cor_g_2':1012,
                                      'filtro_cor_b_2':1013,
                                      'filtro_mass_2':1014,
                                      'filtro_cor_r_3':1021,
                                      'filtro_cor_g_3':1022,
                                      'filtro_cor_b_3':1023,
                                      'filtro_massa_3':1024
                                  })
        return self._widget







if __name__ == '__main__':
    Builder.load_string(open('mainwidget.kv',encoding='utf-8').read(),rulesonly=True)
    Builder.load_string(open('popups.kv', encoding='utf-8').read(), rulesonly=True)
    MainApp().run()
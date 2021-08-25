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
        self.modbus_addrs = [
        {'name': 'estado_atuador', 'description': 'Atuador mecânico que posiciona objetos na esteira (1 - ativo | 0 - inativo)', 'unit': 'ºC', 'adress': 801, 'type': 'coil','mult':1},
        {'name': 'bt_Desliga/Liga', 'description': 'Botão NF Liga/Desliga do processo: (1 - Desliga | 0 - Liga', 'unit': 'ºC', 'adress': 802, 'type': 'coil','mult':1},
        {'name': 't_part', 'description': 'Tempo de partida do motor', 'unit': 'ºC', 'adress': 798, 'type': 'holding','mult':1},
        {'name': 'freq_des', 'description':'Frequência de operação desejada para o motor (prop. à rotação)', 'unit': 'ºC', 'adress': 799, 'type': 'holding','mult':1},
        {'name': 'freq_mot', 'description':'Frequência do motor medida', 'unit': 'ºC', 'adress': 800, 'type': 'input','mult':1},
        {'name': 'tensao', 'description': 'Tensão da rede', 'unit': 'ºC', 'adress': 801, 'type': 'input','mult':1},
        {'name': 'rotacao', 'description': 'Rotação do motor', 'unit': 'ºC', 'adress': 803, 'type': 'input','mult':1},
        {'name': 'pot_entrada', 'description': 'Potência ativa de entrada do inversor', 'unit': 'ºC', 'adress': 804, 'type': 'input','mult':1},
        {'name': 'corrente', 'description': 'Corrente de entrada do inversor (RMS)', 'unit': 'ºC', 'adress': 805, 'type': 'input','mult':1},
        {'name': 'temp_estator', 'description': 'Temperatura do estator do motor', 'unit': 'ºC', 'adress': 806, 'type': 'input','mult':1},
        {'name': 'vel_esteira', 'description': 'Velocidade linear da esteira', 'unit': 'ºC', 'adress': 807, 'type': 'input','mult':1},
        {'name': 'carga', 'description': 'Peso normalizado do objeto gerado', 'unit': 'ºC', 'adress': 808, 'type': 'input','mult':1},
        {'name': 'peso_obj', 'description': 'Peso do objeto', 'unit': 'ºC', 'adress': 809, 'type': 'input','mult':1},
        {'name': 'cor_obj_R', 'description': 'Componente vermelha da cor lida pelo sensor', 'unit': 'ºC', 'adress': 810, 'type': 'input','mult':1},
        {'name': 'cor_obj_G', 'description': 'Componente verde da cor lida pelo sensor', 'unit': 'ºC', 'adress': 811, 'type': 'input','mult':1},
        {'name': 'cor_obj_B', 'description': 'Componente azul da cor lida pelo sensor', 'unit': 'ºC', 'adress': 812, 'type': 'input','mult':1},
        {'name': 'numObj_est_1', 'description': 'Número de objetos aguardando retirada na esteira 1', 'unit': 'ºC', 'adress': 813, 'type': 'input','mult':1},
        {'name': 'numObj_est_2', 'description': 'Número de objetos aguardando retirada na esteira 2', 'unit': 'ºC', 'adress': 814, 'type': 'input','mult':1},
        {'name': 'numObj_est_3', 'description': 'Número de objetos aguardando retirada na esteira 3', 'unit': 'ºC', 'adress': 815, 'type': 'input','mult':1},
        {'name': 'numObj_est_nc', 'description': 'Número de objetos aguardando retirada na esteira NC', 'unit': 'ºC', 'adress': 816, 'type': 'input','mult':1},
        {'name': 'filtro_est_1', 'description': 'Tipo de filtro utilizado na esteira 1: True para cor e False para massa', 'unit': 'ºC', 'adress': 901, 'type': 'coil','mult':1},
        {'name': 'filtro_est_2', 'description': 'Tipo de filtro utilizado na esteira 2: True para cor e False para massa', 'unit': 'ºC', 'adress': 902, 'type': 'coil','mult':1},
        {'name': 'filtro_est_3', 'description': 'Tipo de filtro utilizado na esteira 3: True para cor e False para massa', 'unit': 'ºC', 'adress': 903, 'type': 'coil','mult':1},
        {'name':'filtro_cor_r_1','description':'Componente vermelha do filtro de cor da esteira 1 (0 ou 255)','unit':' ','adress':1001,'type':'holding','mult':1},
        {'name': 'filtro_cor_g_1', 'description': 'Componente verde do filtro de cor da esteira 1 (0 ou 255)', 'unit': 'ºC', 'adress': 1002,'type':'holding','mult':1},
        {'name': 'filtro_cor_b_1', 'description': 'Componente azul do filtro de cor da esteira 1 (0 ou 255)', 'unit': 'ºC', 'adress': 1003,'type':'holding','mult':1},
        {'name': 'filtro_massa_1', 'description': 'Valor do filtro de massa da esteira 1 [massa(obj) >= filtro_massa]', 'unit': 'ºC', 'adress': 1004,'type':'holding','mult':1},
        {'name': 'filtro_cor_r_2', 'description': 'Componente vermelha do filtro de cor da esteira 1 (0 ou 255)', 'unit': 'ºC', 'adress': 1011, 'type': 'holding','mult':1},
        {'name': 'filtro_cor_g_2', 'description': 'Componente verde do filtro de cor da esteira 1 (0 ou 255)', 'unit': 'ºC', 'adress': 1012, 'type': 'holding','mult':1},
        {'name': 'filtro_cor_b_2', 'description': 'Componente azul do filtro de cor da esteira 1 (0 ou 255)', 'unit': 'ºC', 'adress': 1013, 'type': 'holding','mult':1},
        {'name': 'filtro_massa_2', 'description': 'Valor do filtro de massa da esteira 2 [massa(obj) >= filtro_massa]', 'unit': 'ºC', 'adress': 1014, 'type': 'holding','mult':1},
        {'name': 'filtro_cor_r_3', 'description': 'Componente vermelha do filtro de cor da esteira 1 (0 ou 255)', 'unit': 'ºC', 'adress': 1021, 'type': 'holding','mult':1},
        {'name': 'filtro_cor_g_3', 'description': 'Componente verde do filtro de cor da esteira 1 (0 ou 255)', 'unit': 'ºC', 'adress': 1022, 'type': 'holding','mult':1},
        {'name': 'filtro_cor_b_3', 'description': 'Componente azul do filtro de cor da esteira 1 (0 ou 255)', 'unit': 'ºC', 'adress': 1023, 'type': 'holding','mult':1},
        {'name': 'filtro_massa_3', 'description': 'Valor do filtro de massa da esteira 3 [massa(obj) >= filtro_massa]', 'unit': 'ºC', 'adress': 1024, 'type': 'holding','mult':1}
        ]
        self._widget = MainWidget(vel_ramp=1000, server_ip='127.0.0.1', server_port=9000, tags=self.modbus_addrs)
        return self._widget







if __name__ == '__main__':
    Builder.load_string(open('mainwidget.kv',encoding='utf-8').read(),rulesonly=True)
    Builder.load_string(open('popups.kv', encoding='utf-8').read(), rulesonly=True)
    Builder.load_string(open('datacards.kv', encoding='utf-8').read(), rulesonly=True)
    MainApp().run()
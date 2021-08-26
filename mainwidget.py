from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar
from popups import ModbusPopup, ConfigPopup
from pyModbusTCP.client import ModbusClient
from threading import Thread
from time import sleep
from datacards import CardCoil,CardInputRegister,CardHoldingRegister
from datetime import datetime
import random


class MainWidget(MDScreen):
    """
    Widget principal da aplicação
    """
    _updateThread = None
    _updateWidgets = True
    _tags = {}

    def __init__(self,**kwargs):
        """
        Construtor do Widget principal
        """
        super().__init__()
        self._velramp = kwargs.get('vel_ramp')
        self._serverIP = kwargs.get('server_ip')
        self._serverPort = kwargs.get('server_port')
        self._modbusPopup = ModbusPopup(self._serverIP,self._serverPort)
        self._configPopup = ConfigPopup(self._velramp)
        self._modbusClient = ModbusClient(host=self._serverIP, port=self._serverPort)
        self._tags = kwargs.get('tags')
        self._meas = {}
        self._meas['timestamp'] = None
        self._meas['values'] = {}
        for tag in self._tags:
            plot_color = (random.random(),random.random(),random.random(),1)
            tag['color'] = plot_color


        for tag in self._tags:
            if tag['type'] == 'input':
                self.ids.modbus_data.add_widget(CardInputRegister(tag,self._modbusClient))
            elif tag['type'] == 'holding':
                self.ids.act_planta.add_widget(CardHoldingRegister(tag,self._modbusClient))
            elif tag['type'] == 'coil':
                self.ids.act_planta.add_widget(CardCoil(tag,self._modbusClient))



    def config_button(self, button):
        self._configPopup.open()
        Snackbar(text='Teste1').open()

    def conect_button(self, button):
        self._modbusPopup.open()


    def startDataRead(self,ip,port):
        """
        Método utilizado para a configuração do IP e porta
        do servidor MODBUS e inicializar uma thread para a
        leitura dos dados e atualização da interface gráfica
        :param ip: Ip do servidor MODBUS
        :param port: Porta do serviço
        """

        self._serverIP = ip
        self._serverPort = int(port)
        self._modbusClient.host = self._serverIP
        self._modbusClient.port = self._serverPort
        try:
            self._modbusClient.open()
            if self._modbusClient.is_open():
                self._updateThread = Thread(target=self.updater)
                self._updateThread.start()
                Snackbar(text='[color=#000000] Conexão Realizada [/color]', bg_color=(0,1,0,1)).open()
                self.ids.status_con.source = 'imgs/conectado.png'
                self._modbusPopup.dismiss()
            else:
                self._modbusClient.last_error()
                self._modbusPopup.setInfo('Falha na Conexão com o Servidor')

        except Exception as e:
            print('Erro: ', e.args)


    def updater(self):
        """"
        Método que invoca as rotinas de leitura, atualização da interface
        e inserção dos dados no Banco de Dados
        """
        try:
            while self._updateWidgets:
                self.readData() #leitura de dados
                self.updateGUI()
                # Inserir os Dados no BD
                sleep(self._velramp/1000)

        except Exception as e:
            self._modbusClient.close()
            Snackbar(text='Conexão Encerrada',bg_color=(1,0,0,1)).open()
            self.ids.status_con.source = 'imgs/desconectado.png'
            print('Erro: ', e.args)

    def readData(self):
        """
        Método para a leitura dos dados por meio do protocolo MODBUS
        """
        self._meas['timestamp'] = datetime.now()

        for card in self.ids.modbus_data.children:
            if card.tag['type'] == 'input':
                self._meas['values'][card.tag['name']] = card.update_data()

        for card in self.ids.act_planta.children:
            if card.tag['type'] == 'holding' or card.tag['type'] == 'coil':
                self._meas['values'][card.tag['name']] = card.update_data()

    def updateGUI(self):
        """
        Método para atualização da interface gráfica a partir dos dados lidos
        """
        # Atualização dos Labels
        self.ids['info_cor'].text = 'Nenhum Objeto'
        self.ids['info_cor'].color = 0, 0, 0, 1
        self.ids['img_peca'].source = 'imgs/load.png'


        R = G = B = 0

        for card in self.ids.modbus_data.children:
            if card.tag['address'] in [813,814,815,816]:
                self.ids[card.tag['name']].text = str(self._meas['values'][card.tag['name']])
            if card.tag['address'] == 809:
                self.ids[card.tag['name']].text = str(self._meas['values'][card.tag['name']]) + ' Kg'
            if card.tag['address'] == 810:
                R = self._meas['values'][card.tag['name']]
            if card.tag['address'] == 811:
                G = self._meas['values'][card.tag['name']]
            if card.tag['address'] == 812:
                B = self._meas['values'][card.tag['name']]


        if R == G == B == 0:
            self.ids['info_cor'].text = 'Preto'
            self.ids['info_cor'].color = 0, 0, 0, 1
            self.ids['img_peca'].source = 'imgs/peca.png'

        if R == G == B == 0:
            self.ids['info_cor'].text = 'Branco'
            self.ids['info_cor'].color = 0.5, 0.5, 0.5, 1
            self.ids['img_peca'].source = 'imgs/peca.png'

        if R == G > B:
            self.ids['info_cor'].text = 'Amarelo'
            self.ids['info_cor'].color = 1,1,0,1
            self.ids['img_peca'].source = 'imgs/peca.png'


        if R == B > G:
            self.ids['info_cor'].text = 'Rosa'
            self.ids['info_cor'].color = 1,0,1,1
            self.ids['img_peca'].source = 'imgs/peca.png'


        if B == G > R:
            self.ids['info_cor'].text = 'Ciano'
            self.ids['info_cor'].color = 0,1,1,1
            self.ids['img_peca'].source = 'imgs/peca.png'

        if R > G and R > B:
            self.ids['info_cor'].text = 'Vermelho'
            self.ids['info_cor'].color = 1,0,0,1
            self.ids['img_peca'].source = 'imgs/peca.png'


        if G > R and G > B:
            self.ids['info_cor'].text = 'Verde'
            self.ids['info_cor'].color = 0,1,0,1
            self.ids['img_peca'].source = 'imgs/peca.png'

        if B > G and B > R:
            self.ids['info_cor'].text = 'Azul'
            self.ids['info_cor'].color = 0,0,1,1
            self.ids['img_peca'].source = 'imgs/peca.png'





    def stopRefresh(self):
        self._updateWidgets = False













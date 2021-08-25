from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import Snackbar
from kivy.lang import Builder
from popups import ModbusPopup, ConfigPopup
from pyModbusTCP.client import ModbusClient
from kivy.core.window import Window
from threading import Thread
from time import sleep
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
        self._meas = {}
        self._meas['timestamp'] = None
        self._meas['values'] = {}
        for key.value in kwargs.get('modbus_addrs').items():
            plot_color = (random.random(),random.random(),random.random(),1)
            self._tags[key] = {'addr': value, 'color': plot_color}


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
            print(self._modbusClient.host, type(self._modbusClient.host))
            print(self._modbusClient.port, type(self._modbusClient.port))
            self._modbusClient.open()
            if self._modbusClient.is_open():
                self._updateThread = Thread(target=self.updater)
                self._updateThread.start()
                Snackbar(text='Conexão Realizada').open()
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
                self.readData()
                # Atualizar a interface
                # Inserir os Dados no BD
                sleep(self._velramp/1000)

        except Exception as e:
            self._modbusClient.close()
            Snackbar(text='Conexão Encerrada').open()
            print('Erro: ', e.args)

    def readData(self):
        """
        Método para a leitura dos dados por meio do protocolo MODBUS
        """
        self._meas['timestamp'] = datetime.now()
        for key,value in self._tags.items():
            self._meas['values'][key] = self._modbusClient.read_holding_registers(value['addr'],1)[0]
















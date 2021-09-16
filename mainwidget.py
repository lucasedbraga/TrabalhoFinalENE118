from logging import info
from os import name
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar
from popups import ModbusPopup, ConfigPopup 
from pyModbusTCP.client import ModbusClient
from threading import Thread, Lock
from time import sleep
from datacards import CardCoil,CardInputRegister,CardHoldingRegister
from datetime import datetime
import random
from kivy.clock import Clock
from functools import partial
from sqlalchemy import engine
from db import Session, Base, engine
from models import DadosCLP
from kivy_garden.graph import LinePlot
from timeseriesgraph import  TimeSeriesGraph


class MainWidget(MDScreen):
    """
    Widget principal da aplicação
    """
    _updateThread = None
    _updateWidgets = True
    _tags = {}
    _max_points = 20

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
        self._session = Session()
        Base.metadata.create_all(engine)
        self._lock = Lock()

        for tag in self._tags:
            if tag['type'] == 'input':
                self.ids.modbus_data.add_widget(CardInputRegister(tag,self._modbusClient))
            elif tag['type'] == 'holding':
                self.ids.act_planta.add_widget(CardHoldingRegister(tag,self._modbusClient))
            elif tag['type'] == 'coil':
                self.ids.act_planta.add_widget(CardCoil(tag,self._modbusClient))
            
            if tag['address'] in [809,810,811,812]:
                endereco = tag['address']
                if endereco == 809:
                    plot_color = (0,0,0,1)
                    tag['color'] = plot_color
                if endereco == 810:
                    plot_color = (1,0,0,1)
                    tag['color'] = plot_color
                if endereco == 811:
                    plot_color = (0,1,0,1)
                    tag['color'] = plot_color
                if endereco == 812:
                    plot_color = (0,0,1,1)
                    tag['color'] = plot_color
                
                cb = LabeledCheckBoxHistGraph()
                cb.ids.label.text = tag['name']
                cb.ids.label.color = tag['color']
                cb.id = tag['name']
                self.ids.sensores.add_widget(cb)




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
                self._guardar_dados = Thread(target=self.guardar_dados)
                self._updateThread = Thread(target=self.updater)
                self._updateThread.start()
                self._guardar_dados.start()
                

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
                self.readData() # Leitura de dados
                self.updateGUI() # Atualização da IHM
                self.guardar_dados() # Inserir os Dados no BD
                sleep(500/1000)

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
    
    def updateImage(self,img_src,dt):
        self.ids['img_peca'].source = img_src

    def updateBackground(self,img_src,dt):
        self.ids['img_planta'].source = img_src



    def updateGUI(self,**kwargs):
        """
        Método para atualização da interface gráfica a partir dos dados lidos
        """
        # Atualização dos Labels

        if self._meas['values']['bt_Desliga_Liga'] == True:
            Clock.schedule_once(partial(self.updateBackground, 'imgs/planta_off.png'))
            Clock.schedule_once(partial(self.updateImage, 'imgs/standby.png'))
        else:
            Clock.schedule_once(partial(self.updateBackground,'imgs/planta_on.jpg'))


            self.ids['info_cor'].text = 'Nenhum Objeto'
            self.ids['info_cor'].color = 0, 0, 0, 1
            self.ids['info_velramp'].text = f"Vel.Esteira: {self._meas['values']['vel_esteira']} m/s"
            self.ids['info_tensaorede'].text = f"Tensão: {self._meas['values']['tensao']} V"
            Clock.schedule_once(partial(self.updateImage,'imgs/load.png'))


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
                Clock.schedule_once(partial(self.updateImage,'imgs/peca_preta.jpg'))

            if R == G == B == 255:
                self.ids['info_cor'].text = 'Branco'
                self.ids['info_cor'].color = 0.5, 0.5, 0.5, 1
                Clock.schedule_once(partial(self.updateImage,'imgs/peca_branca.png'))

            if R == G and R > B:
                self.ids['info_cor'].text = 'Amarelo'
                self.ids['info_cor'].color = 1,1,0,1
                Clock.schedule_once(partial(self.updateImage,'imgs/peca_rg.jpg'))

            if R == B and R > G:
                self.ids['info_cor'].text = 'Rosa'
                self.ids['info_cor'].color = 1,0,1,1
                Clock.schedule_once(partial(self.updateImage,'imgs/peca_rb.jpg'))

            if B == G and B > R:
                self.ids['info_cor'].text = 'Ciano'
                self.ids['info_cor'].color = 0,1,1,1
                Clock.schedule_once(partial(self.updateImage,'imgs/peca_gb.jpg'))


            if R > G and R > B:
                self.ids['info_cor'].text = 'Vermelho'
                self.ids['info_cor'].color = 1,0,0,1
                Clock.schedule_once(partial(self.updateImage,'imgs/peca_r.png'))



            if G > R and G > B:
                self.ids['info_cor'].text = 'Verde'
                self.ids['info_cor'].color = 0,1,0,1
                Clock.schedule_once(partial(self.updateImage,'imgs/peca_g.jpg'))

            if B > G and B > R:
                self.ids['info_cor'].text = 'Azul'
                self.ids['info_cor'].color = 0,0,1,1
                Clock.schedule_once(partial(self.updateImage,'imgs/peca_b.png'))






    def stopRefresh(self):
        self._updateWidgets = False

    def guardar_dados(self):
        """
        Método para a leitura dos dados do servidor e armazenamento no BD
        """
        try:
            self._modbusClient.is_open()
            data = {}
            data['timestamp'] = datetime.now()
            for tag in self._tags:
                data[tag['name']] = self._meas['values'][tag['name']]
            dado = DadosCLP(**data)
            self._lock.acquire()
            self._session.add(dado)
            self._session.commit()
            self._lock.release()



        except Exception as e:
            print("Erro ao Guardar os Dados: ", e.args)


    def getDataDB(self):
        """
        Método que coleta as informações da interface fornecidas pelo usuário 
        e requisita a busca no BD
        """
        try:
            init_t = self.parseDTString(self.ids.txt_init_time.text)
            final_t = self.parseDTString(self.ids.txt_final_time.text)
            cols = []
            for sensor in self.ids.sensores.children:
                if sensor.ids.checkbox.active:
                    cols.append(sensor.id)
            if init_t is None or final_t is None or len(cols) ==0 :
                return

            cols.append('timestamp')
            result = self._session.query(DadosCLP).filter(DadosCLP.timestamp.between(init_t,final_t)).all()

            
            self.ids.graph_cor.clearPlots()
            self.ids.graph_peso.clearPlots()

            result_fmt_list = [obj.get_attr_printable_list() for obj in result]

            info_timestamp = []
            info_R = []
            info_G = []
            info_B = []
            info_peso = []
            for registro in result_fmt_list:
                info_timestamp.append(registro[1])
                info_R.append(registro[15])
                info_G.append(registro[16])
                info_B.append(registro[17])
                info_peso.append(registro[14])

            plot_rgb = {'cor_obj_R':info_R,'cor_obj_G':info_G,'cor_obj_B':info_B}

            for grupo,value in plot_rgb.items():
                for tag in self._tags:
                    if grupo == tag['name'] and grupo in cols:
                        p = LinePlot(line_width = 1.5, color=tag['color'])
                        p.points  = [(x,value[x]) for x in range(0,len(value))]
                        self.ids.graph_cor.add_plot(p)

            if 'peso_obj' in cols:
                p = LinePlot(line_width = 1.5, color=(0,0,0,1))
                p.points  = [(x,info_peso[x]) for x in range(0,len(info_peso))]
                self.ids.graph_peso.add_plot(p)


            self.ids.graph_cor.update_x_labels([x for x in info_timestamp])
            self.ids.graph_peso.update_x_labels([x for x in info_timestamp])

        except Exception as e:
            print('Erro ao plotar a curva: ', e.args)
    
    def parseDTString(self,datetime_str):
        """
        Método que converte a string inserida pelo usuário para o formato utilizado
        na busca dos dados no BD
        """
        try:
            d = datetime.strptime(datetime_str,'%d/%m/%Y %H:%M:%S')
            return d.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print('Erro: ', e.args)

       

class LabeledCheckBoxHistGraph(BoxLayout):
    pass













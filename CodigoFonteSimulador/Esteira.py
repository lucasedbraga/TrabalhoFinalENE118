from Motor import Motor
import math
import numpy as np
from random import randint, random, randrange
from datetime import datetime
class Esteira:
    """
    class esteira

    Adicionar à esteira a Fila de Caixas (contendo dados das caixas e número máximo de caixas na esteira)

    Adicionar à esteira o medidor que calcula o tempo entre as caixas

    Adicionar o sensor de posição à esteira (definir a distância através do timer e da velocidade da esteira)

    """

    def __init__(self, tick, actuator=True, bt_pressed=False, tamEsteira=15, pesoMax=10):
        """
        class constructor
        dictionary to initialize motor params
        """
        self.__posSensor = False
        self.__ftime = 1 #indica se o processo está sendo executado pela primeira vez a fim de gerar a caixa sem ter que esperar pelo ttime
        self.__tick = tick
        self.__etick = 0
        self.__act = actuator
        self.__load = 0
        self.__is_pressed = bt_pressed
        self.__obj = {}
        self.__tamEsteira = tamEsteira  # [m]
        self.__pesoMax = pesoMax
        self._reixo = 1 #[m]
        self.__ttime = 0
        self.__pulseTime = 0
        self.__motorDic = {"state": not bt_pressed, "tensao": 220, "eff": 0.8, "polo": 4, "costheta": 0.8, "horsepower": 3, "slipNom": 0.05,
                           "load": 0.5, "frequencia": 60, "opFrequencia": 60, "TempAmbiente": 24, "tal": 100, "tstart": 3}
        self.motor = Motor(**self.__motorDic)

    """
    return data to registers
    """

    def get_pos_sensor(self):
        return self.__posSensor

    def getActuatorState(self):
        return self.__act

    def getSpeed(self):
        return int(self.__speed*100)

    def getLoad(self):
        return int(self.__load*100)

    def getTick(self):
        return self.__tick

    def getETick(self): #adicionada
        return self.__etick

    def getTTime(self): #adicionada
        return self.__ttime

    def getButtonState(self):
        return self.__is_pressed

    def setActuator(self, state):
        self.__act = state
        
    def button(self, is_pressed):
        self.__is_pressed = is_pressed
        
    def CalculaSpeed(self):
        self.__speed = 2*0.008*self.motor.getRotacao()*(math.pi/30)*self._reixo #modificada

    def travelTime(self):  # avaliar a varredura de valores do ttime (min 10s) modular speed
        if not self.__speed == 0:
            self.__ttime = self.__tamEsteira/(self.__speed)
        else:
            self.__ttime = 0
            
    def objGenerator(self):
        if not self.__is_pressed:
            if self.__act:
                if (self.__etick >= self.__ttime) or (self.__ftime == 1):
                    self.__ftime = 0
                    self.__obj.clear()
                    self.__obj['Peso'] = self.__pesoMax*random() + 1 
                    self.__obj['width'] = 1.15*randint(2, 3) # 0.4 a 0.8 m
                    self.__obj['R'] = randrange(0,256,step=255)
                    self.__obj['G'] = randrange(0,256,step=255)
                    self.__obj['B'] = randrange(0,256,step=255)                    
                    self.__isDict = True
                else:                      
                    self.__isDict = False
            else:
                self.__isDict = False
        else:
            self.__isDict = False

    def getObj(self): #Classe adicionada TESTE
        return self.__obj
    
    def setObj(self,obj):   #Classe adicionada TESTE
        self.__obj = obj
            
    def CalculaCarga(self):
        if self.__isDict:
            self.__load = self.__obj['Peso']/self.__pesoMax
        else:
            self.__load = 0
        
    # tempo de alto no minimo 2 segundo e max 5 segundos (modular largura do objeto)
    def pulseTime(self):
        if not self.__speed == 0:
            if self.__isDict:
                self.__pulseTime = self.__obj['width']/self.__speed

    def weightSensor(self):
        if not self.__speed == 0:
            if self.__etick >= self.__ttime/2 and self.__etick < self.__ttime/2 + self.__pulseTime:
                return self.__obj['Peso']
            else:
                return 0
        else:
            return 0

    def colorSensor(self):
        color = (0,0,0)
        if not self.__speed == 0:
            if self.__etick >= self.__ttime/2 and self.__etick < self.__ttime/2 + self.__pulseTime:
                color = (self.__obj['R'],self.__obj['G'],self.__obj['B'])
        return color
    
    """ and (not self.__is_pressed) """

    def endCourse(self): 
        if self.__etick >= self.__ttime:
            if self.__isDict:
                self.__posSensor = True
            self.__etick = 0
            
    def EsteiraSimulation(self, frequencia, t_partida, act_state, bt_state,grab_sensor):
        """
        set motor/treadmill params upon user frequency input
        """
        if frequencia == 0:
            bt_state = True
            
        if grab_sensor == True:
            act_state = False
            self.__posSensor = False


        self.__etick = self.__etick + self.__tick
        self.setActuator(act_state)
        self.button(bt_state)
                
        self.motor.setTStart(t_partida)
        if self.__is_pressed:
            freq = 0
        else:
            freq = self.motor.partida(not bt_state, frequencia, self.__tick)
        self.motor.TorqueNom()
        self.motor.setOpFrequencia(freq)
        self.motor.wSincronaOperacao()
        self.motor.TorqueVazio()
        self.motor.setLoad(self.__load)
        self.motor.Torque()
        self.motor.Rotacao()
        self.motor.OutPower()
        self.motor.InPower()
        self.motor.CalculaCorrente()
        self.motor.Temperature(self.__tick)

        self.CalculaSpeed()
        self.travelTime()
        self.objGenerator()
        self.CalculaCarga()
        self.pulseTime()
        self.weightSensor()
        self.colorSensor()
        self.endCourse()
        
        
        # print(self.__pulseTime)
        # print(self.presenceSensor())
        # print(self.weightSensor())
        # print(self.colorSensor())
        # print(self.__ttime)
        # print(self.__speed)
        # print(self.__obj)
        # print('\n')

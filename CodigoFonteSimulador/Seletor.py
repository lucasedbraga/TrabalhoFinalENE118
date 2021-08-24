from collections import deque
from typing import NewType
from time import sleep
import random


class Seletor:
	"""
	Classe onde é implementado o robô seletor responsável por colocar as caixas em suas respectivas estantes
	"""

	def __init__(self, tick, actuator = False, ttrabalho = 5, grabSensor = False, num_esteiras_saida = 3, max_caixas = 30):
		"""
		construtor da classe
		dicionario para inicializar os parametros do motor
		obter o tick da esteira
		obter o atuador da esteira -> o robô só liga se a esteira também estiver ligada.
		"""
		self.__filas = [{'fila':deque(),'filter_type':False,'regras':{'R':0,'G':0,'B':0,'Peso':20},'tsaida':5,'tcorrido':0},{'fila':deque(),'filter_type':False,'regras':{'R':0,'G':0,'B':0,'Peso':20},'tsaida':5,'tcorrido':0},{'fila':deque(),'filter_type':False,'regras':{'R':0,'G':0,'B':0,'Peso':20},'tsaida':5,'tcorrido':0},{'fila':deque(),'regras':None,'tsaida':15,'tcorrido':0}]
		self.__tick = tick # delta_t do monitoramento do sistema. Utilizado para atualizar o estado das variáveis e para
						   # plotagem dos gráficos
		#self.__etick = 0
		self.__objectColor = () #armazena a cor do objeto atual. Obter este valor da esteira
		self.__act = actuator #estado do atuador, true ou false
		self.__ttrabalho = ttrabalho # tempo que o manipulador demora para pegar a caixa, deixá-la em uma das prateleiras e 
									 # voltar para a posição original. Obs: Dois objetos não devem ter uma distância entre
									 # entre si menor do que v_esteira[m/s]*dutyCycle[s]. se isto ocorrer, a esteira deve
									 # parar e esperar o manipulador terminar um duty cycle antes de retomar. Se o intervalo
									 # for maior, a esteira retoma o funcionamento logo após o objeto ser retirado.
		self.__grabSensor = grabSensor # sensor que detecta se o manipulador está segurando um objeto ou não
		self.__max_caixas = max_caixas

		pass

	def get_filas(self):
		return self.__filas

	def getTick(self):
		return self.__tick

	def getObjectColor(self):
		return self.__objectColor

	def get_ttrabalho(self):
		return self.__ttrabalho

	def getActuator(self):
		return self.__act
	
	def getGrabSensor(self):
		return self.__grabSensor

	def set_ttrabalho(self,newDuty):
		"""
		Seta o intervalo de tempo do duty cycle com um mínimo de 5s e um máximo de 120s.
		"""
		if(newDuty<5):
			return 5
		elif(newDuty>120):
			return 120
		else:
			return NewType

	def set_regras(self,fila, regras):
		self.__filas[fila]['regras'] = regras #regras deve ser no formato {'R':0,'G':255,'B':0}; {'tamanho': 1}; {'peso': 1}


	def set_filter_type(self,fila, filter_type):
		self.__filas[fila]['filter_type'] = filter_type

	def objectDetector(self):
		"""
		Detecta o objeto na posição final da esteira e recebe da esteira a cor, tamanho e peso deste.

		Recebe da Fila de Caixas os Parâmetros da caixa atual (acrescentar este parâmetro à operação da esteira)
		"""

		#identifica a caixa

		#Pega a caixa
		self.__grabSensor = True
		# print("transportanto caixa")

		#Realiza metade do duty cycle
		sleep(self.__dutyCycle/2)

		#Coloca a caixa na Fila correspondente
		self.__grabSensor = False
		# print("caixa transportada")

		#Adicionar a caixa à fila

		#Realiza o restante do duty cycle
		sleep(self.__dutyCycle/2)

	def SeletorSimulation(self,etick,posSensor,objeto_atual):
		"""
		Simulação do Seletor
		"""
		#self.__etick = self.__etick + self.__tick
		if(posSensor):
			self.gotTime = etick
			self.__grabSensor = True
		elif(self.__grabSensor):
			if(etick - self.gotTime >= (self.__ttrabalho)/2):
				for fila in self.__filas:
					if fila['regras'] is None:
						break
					if(len(fila['fila']) >= self.__max_caixas): #A fila extra entraria aqui
						self.__grabSensor = False
						continue
					if((fila['filter_type']  == True) and objeto_atual['R'] == fila['regras']['R'] and objeto_atual['G'] == fila['regras']['G'] and objeto_atual['B'] == fila['regras']['B']):
						fila['fila'].appendleft(objeto_atual)
						self.__grabSensor = False
						return
					if((fila['filter_type'] == False) and objeto_atual['Peso'] >=fila['regras']['Peso']):
						fila['fila'].appendleft(objeto_atual)
						self.__grabSensor = False
						return
				self.__filas[3]['fila'].appendleft(objeto_atual)
				self.__grabSensor = False
				return

	def remove_obj(self,travel_time):
		for fila in self.__filas:
			fila['tcorrido']+=self.__tick
			if fila['tcorrido'] >= fila['tsaida'] and len(fila['fila'])>0:
				fila['tsaida'] = travel_time*self.__max_caixas/(len(fila['fila']))*random.random()
				fila['fila'].pop()
				fila['tcorrido'] = 0
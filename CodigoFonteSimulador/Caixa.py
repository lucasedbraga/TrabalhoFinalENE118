class Caixa:
	"""
	Classe onde são implementados os objetos (caixas) manipulados na linha de produção.
	OPT -> Como, em geral, lidaremos com várias caixas, os métodos para a implementação de filas de caixas também serão implementados aqui.
	"""
	def __init__(self, tamanho = -1, maxPrateleira = 1):
		self.__maxPrateleira = maxPrateleira #Número máximo de caixas na prateleira
		self.__tamanho = tamanho #tamanho da fila
		self.__caixas = []

		#deque
		
	def getTamanho(self):
		return self.__tamanho + 1

	def getMaxPrateleira(self):
		return self.__maxPrateleira

	def setMaxPrateleira(self,novoMax):
		self.__maxPrateleira = novoMax
	
	def insereCaixa(self,novaCaixa):
		if(self.__tamanho >= self.__maxPrateleira - 1):
			print("número máximo de caixas atingido") 
			return False
		else:
			self.__caixas.insert(0,novaCaixa)
			print("Caixa inserida na fila")
			self.__tamanho = self.__tamanho + 1
	
	def removeCaixa(self):
		if(self.__tamanho == -1):
			print("A fila está vazia")
		else:
			self.__caixas.pop()
			self.__tamanho = self.__tamanho - 1

	def imprimeFila(self):
		for i in self.__caixas:
			print(i)

	

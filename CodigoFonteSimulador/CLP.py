from pyModbusTCP.server import DataBank, ModbusServer
from Esteira import Esteira
from Seletor import Seletor
from time import sleep
from time import perf_counter
from random import randrange
class CLP():
    """
    class CLP - Server - ModBus TCP
    attribute: tick : CLP cycle time
    """
    __tick = 0.1

    def __init__(self,host,port):
        """
        class constructor
        param: host: server IP address
        param: port : server port
        """
        self.__server = ModbusServer(host=host, port=port, no_block=True)
        self.__db = DataBank()
        self.__esteira = Esteira(self.__tick)
        self.__seletor = Seletor(self.__tick)
        
        self.__db.set_words(799,(self.__esteira.motor.getOpFrequencia()/10,))  
        self.__db.set_words(798,(self.__esteira.motor.getTStart()*10,))       
        self.__db.set_bits(800,(self.__esteira.motor.getState(),))       
        self.__db.set_bits(801,(self.__esteira.getActuatorState(),))
        self.__db.set_bits(802,(self.__esteira.getButtonState(),))
        self.__db.set_words(808,(self.__esteira.getLoad(),))

        self.__db.set_words(1004,(20,))
        self.__db.set_words(1014,(20,))
        self.__db.set_words(1024,(20,))

    def Connection(self):
        """
        starts server
        listen client
        """
        self.__server.start()
        print('Simulador Online... Ctrl+C para parar')
        #actState = self.__db.get_bits(801)[0] #linha adicionada TESTE
        while True:
            try:
                self.DoService()
            except Exception as e:
                print("Error: ",e.args)

    def rgb_to_hex(self):
        pass

    def hex_to_rgb(self):
        pass
    
    def DoService(self):
        """
        serve client
        simulate esteira
        set esteira/motor params thru registers
        random noise added when reading data 
        """
        t0 = perf_counter()
        actState = self.__db.get_bits(801)[0] 
        frequency = self.__db.get_words(799)[0]
        t_partida = self.__db.get_words(798)[0]/10
        bt_state = self.__db.get_bits(802)[0]

        self.__seletor.set_filter_type(0,self.__db.get_bits(901)[0])
        self.__seletor.set_filter_type(1,self.__db.get_bits(902)[0])
        self.__seletor.set_filter_type(2,self.__db.get_bits(903)[0])

        for fila in range(0,3):
            self.__seletor.set_regras(fila,
            {
            'R':self.__db.get_words(1001 + 10*fila)[0],
            'G':self.__db.get_words(1002 + 10*fila)[0],
            'B':self.__db.get_words(1003 + 10*fila)[0],
            'Peso':self.__db.get_words(1004 + 10*fila)[0]}
            )


        self.__esteira.EsteiraSimulation(frequency, t_partida,actState,bt_state,self.__seletor.getGrabSensor())

        self.__seletor.SeletorSimulation(self.__esteira.getETick(),self.__esteira.get_pos_sensor(),self.__esteira.getObj())

        self.__seletor.remove_obj(self.__esteira.getTTime())        

        self.__db.set_words(801, (self.__esteira.motor.getTensao()+ randrange(-3,4),)) #Endereço 801?
        self.__db.set_words(802, (self.__esteira.motor.getTorque(),))
        self.__db.set_words(800,(max(self.__esteira.motor.getOpFrequencia()+ randrange(-3,4),0),))
        self.__db.set_words(803, (max(self.__esteira.motor.getRotacao() + randrange(-3,4),0),))
        self.__db.set_words(804,(max(self.__esteira.motor.getInPower()+ randrange(-3,4),0),))
        self.__db.set_words(805, (max(self.__esteira.motor.getCorrente() + 10*randrange(-2,2),0),))
        self.__db.set_words(806,(max(self.__esteira.motor.getTemperature()+ randrange(-2,3),0),))
        self.__db.set_words(807,(max(self.__esteira.getSpeed()+ 10*randrange(-1,2),0),))
        self.__db.set_words(808,(max(self.__esteira.getLoad()+ 10*randrange(-3,4),0),))
        self.__db.set_words(809,(round(100*self.__esteira.weightSensor(),0),))
        color = self.__esteira.colorSensor()
        self.__db.set_words(810,(color[0],))  
        self.__db.set_words(811,(color[1],)) 
        self.__db.set_words(812,(color[2],))

        self.__db.set_words(813,(len(self.__seletor.get_filas()[0]['fila']),)); #Envia o tamanho da primeira fila
        self.__db.set_words(814,(len(self.__seletor.get_filas()[1]['fila']),)); #Envia o tamanho da segunda fila
        self.__db.set_words(815,(len(self.__seletor.get_filas()[2]['fila']),)); #Envia o tamanho da terceira fila
        self.__db.set_words(816,(len(self.__seletor.get_filas()[3]['fila']),)); #Envia o tamanho da fila NC

        t1 = (perf_counter() - t0)/1000
        sleep(self.__tick - t1)

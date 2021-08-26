from sqlite3.dbapi2 import enable_callback_tracebacks
from pyModbusTCP.client import ModbusClient
from datetime import datetime
from time import sleep
from pyModbusTCP.utils import reset_bit
from sqlalchemy import engine
from tabulate import tabulate 
from threading import Thread, Lock
from db import Session, Base, engine
from models import DadoCPL

class ModbusPersistencia():
    """
    Classe que implementa a funcionalidade de dados
    lidos a partir do protocolo Modbus e também permite a busca de dados históricos
    """
    def __init__(self, server_ip, server_port, tags_addrs, scan_time = 1):
        """
        Construtor
        """
        self._cliente_modbus = ModbusClient(host=server_ip, port=server_port)
        self._scan_time = scan_time
        self._tags_addrs = tags_addrs
        self._session = Session()
        Base.metadata.create_all(engine)
        self._lock = Lock()
        self.guardar_dados = Thread(target=self.guardar_dados)

    def guardar_dados(self):
        """
        Método para a leitura dos dados do servidor e armazenamento no BD
        """
        try:
            print("Persistencia iniciada")
            self._cliente_modbus.open()
            data = {}
            while True:
                data['timestamp'] = datetime.now()
                for tag in self._tags_addrs:
                    data[tag] = self._cliente_modbus.read_holding_registers(self._tags_addrs[tag],1)[0]
                dado = DadoCPL(**data)
                self._lock.acquire()
                self._session.add(dado)
                self._session.comit()
                self._lock.release()
                sleep(self._scan_time)

        except Exception as e:
            print("Erro na persistencia de dados: ", e.args)

    def acesso_dados_historicos(self):
        """
        Método que permite ao usuário acessar dados históricos
        """
        try:
            print("Bem vindo ao sistema de busca de dados históricos")
            while True:
                init = input("Digite o horário inicial para a busca (DD/MM/AAAA HH:MM:SS): ")
                final = input("Digite o horário final para a busca (DD/MM/AAAA HH:MM:SS): ")
                init = datetime.strftime(init,'%d%m%Y %H:%M:%S')
                final = datetime.strftime(final,'%d%m%Y %H:%M:%S')
                self._lock.acquire()
                result = self._session.query(DadoCPL.timestamp.between(init,final)).all()
                result_fmt_list = [obj.get_attr_printable_list() for obj in result]
                self._lock.release()

                print(tabulate(result_fmt_list,headers=DadoCPL.__table__.columns.keys()))

        except Exception as e:
            print("Erro na persistencia de dados: ", e.args)
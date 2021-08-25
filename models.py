from db import Base
from sqlachemy import Column, Integer, DateTime, Float

class DadosCLP(Base):
    """
    Modelo dos dados do CLP
    """
    __tablename = 'dadoclp'
    id = Column(Integer, primary_key = True, autoincrement = True)
    timestamp = Column(DateTime)
    freq_des = Column(Integer/1)
    freq_motor = Column(Integer/10)
    tensao = Column(Integer/1)
    rotacao = Column(Integer/1)
    pot_entrada = Column(Integer/10)
    corrente = Column(Integer/100)
    temp_estator = Column(Integer/10)
    vel_esteira = Column(Integer/100)
    carga = Column(Integer/100)
    peso_obj = Column(Integer/1)
    cor_obj_R = Column(Integer/1)
    cor_obj_G = Column(Integer/1)
    cor_obj_B = Column(Integer/1)
    numObj_est_1 = Column(Integer/1)
    numObj_est_2 = Column(Integer/1)
    numObj_est_3 = Column(Integer/1)
    numObj_est_nc = Column(Integer/1)
    filtro_est_1 = Column(Integer)
    filtro_est_2 = Column(Integer)
    filtro_est_3 =Column(Integer)

from db import Base
from sqlalchemy import Column, Integer, DateTime, Float, Boolean


class DadosCLP(Base):
    """
    Modelo dos dados do CLP
    """
    __tablename__ = 'dadosclp'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime)
    estado_atuador = Column(Boolean)
    bt_Desliga_Liga = Column(Boolean)
    t_part = Column(Float)
    freq_des = Column(Float)
    freq_mot = Column(Float)
    tensao = Column(Float)
    rotacao = Column(Float)
    pot_entrada = Column(Float)
    corrente = Column(Float)
    temp_estator = Column(Float)
    vel_esteira = Column(Float)
    carga = Column(Float)
    peso_obj = Column(Float)
    cor_obj_R = Column(Integer)
    cor_obj_G = Column(Integer)
    cor_obj_B = Column(Integer)
    numObj_est_1 = Column(Integer)
    numObj_est_2 = Column(Integer)
    numObj_est_3 = Column(Integer)
    numObj_est_nc = Column(Integer)
    filtro_est_1 = Column(Boolean)
    filtro_est_2 = Column(Boolean)
    filtro_est_3 = Column(Boolean)
    filtro_cor_r_1 = Column(Integer)
    filtro_cor_g_1 = Column(Integer)
    filtro_cor_b_1 = Column(Integer)
    filtro_massa_1 = Column(Integer)
    filtro_cor_r_2 = Column(Integer)
    filtro_cor_g_2 = Column(Integer)
    filtro_cor_b_2 = Column(Integer)
    filtro_massa_2 = Column(Integer)
    filtro_cor_r_3 = Column(Integer)
    filtro_cor_g_3 = Column(Integer)
    filtro_cor_b_3 = Column(Integer)
    filtro_massa_3 = Column(Integer)

    def get_attr_printable_list(self):
        return [self.id,
                self.timestamp,
                self.estado_atuador,
                self.bt_Desliga_Liga,
                self.t_part,
                self.freq_des,
                self.freq_mot,
                self.tensao,
                self.rotacao,
                self.pot_entrada,
                self.corrente,
                self.temp_estator,
                self.vel_esteira,
                self.carga,
                self.peso_obj,
                self.cor_obj_R,
                self.cor_obj_G,
                self.cor_obj_B,
                self.numObj_est_1,
                self.numObj_est_2,
                self.numObj_est_3,
                self.numObj_est_nc,
                self.filtro_est_1,
                self.filtro_est_2,
                self.filtro_est_3,
                self.filtro_cor_r_1,
                self.filtro_cor_g_1,
                self.filtro_cor_b_1,
                self.filtro_massa_1,
                self.filtro_cor_r_2,
                self.filtro_cor_g_2,
                self.filtro_cor_b_2,
                self.filtro_massa_2,
                self.filtro_cor_r_3,
                self.filtro_cor_g_3,
                self.filtro_cor_b_3,
                self.filtro_massa_3]

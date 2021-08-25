"""
Objetos do SQLalchemy core para realização da conexão e operação do banco de dados
"""
from sqlalchemy import creat_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_CONNECTION = 'sqlite:\\data\data.db?check_same_thread=False'
engine = creat_engine(DB_CONNECTION,echo = False)
Base = declarative_base()
Session - sessionmaker(bind = engine)


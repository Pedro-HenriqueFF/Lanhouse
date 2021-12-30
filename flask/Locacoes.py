from sqlalchemy.orm import backref
from database import db
from sqlalchemy.sql import func
import datetime

class Locacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer,db.ForeignKey('usuario.id'))
    nome_pessoa = db.Column(db.String(100),unique=False,nullable=True)
    id_dispositivo = db.Column(db.Integer,db.ForeignKey('maquina.id'))
    data_locacao = db.Column(db.DateTime,unique=False,nullable=False,default=func.now())
    #tempo_restante
    data_encerramento = db.Column(db.DateTime,unique=False,nullable=True)
    pago = db.Column(db.Boolean,default=False)
from sqlalchemy.orm import backref
from database import db
from sqlalchemy.sql import func

class Locacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer,db.ForeignKey('usuario.id'))
    nome_pessoa = db.Column(db.String(100),unique=False,nullable=True)
    id_maquina = db.Column(db.Integer,db.ForeignKey('maquina.id'))
    data_emprestimo = db.Column(db.DateTime,unique=False,nullable=False,default=func.now())
    data_devolucao = db.Column(db.DateTime,unique=False,nullable=True)

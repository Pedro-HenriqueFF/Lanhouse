from sqlalchemy.orm import backref
from database import db

class Dispositivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=False, nullable=False)
    disponivel = db.Column(db.Integer, default=0)
    locacoes = db.relationship('Locacao',backref='dispositivo',lazy=True)
    def asdict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

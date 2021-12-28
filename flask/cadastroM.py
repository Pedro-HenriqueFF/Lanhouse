from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class cadastroM(FlaskForm):
    nome = StringField('Nome da maquina', validators=[DataRequired()])
    enviar = SubmitField('CADASTRAR')

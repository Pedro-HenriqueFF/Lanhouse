from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class DispositivoForm(FlaskForm):
    nome = StringField('Nome do dispositivo', validators=[DataRequired()])
    enviar = SubmitField('CADASTRAR')
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

class LocacaoForm(FlaskForm):
    nome = StringField('Nome de quem pega emprestado: ', validators=[DataRequired()])
    dispositivo = SelectField('Dispositivo',coerce=int)
    #tempo_locacao
    enviar = SubmitField('CADASTRAR')

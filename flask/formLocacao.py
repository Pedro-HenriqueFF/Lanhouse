from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

class LocacaoForm(FlaskForm):
    nome = StringField('Nome de quem pega emprestado: ', validators=[DataRequired()])
    dispositivo = SelectField('Dispositivo',coerce=int,default=None)
    tempo_locacao = SelectField(u'Tempo de Locação',choices=[('1', '30 minutos'), ('2', '1 hora')],coerce=int,default=None)
    enviar = SubmitField('LOCAR')

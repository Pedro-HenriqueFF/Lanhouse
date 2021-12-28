from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class loginform(FlaskForm):
    usuario = StringField('Nome de usuário', validators=[DataRequired()])
    senha = PasswordField('Senha: ', validators=[DataRequired()])
    enviar = SubmitField('CADASTRAR')

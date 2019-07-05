from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length, Email
from wtforms.fields.html5 import EmailField, DateField


from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Usuário', validators=[
        DataRequired(), Length(1, 64)
    ])
    nascimento = DateField('Data de nascimento', validators=[
        DataRequired()
    ])
    email = EmailField('E-mail', validators=[
        DataRequired()
    ])
    password = PasswordField('Senha', validators=[
        DataRequired()
    ])
    password2 = PasswordField('Confirmar Senha', validators=[
        DataRequired(), EqualTo('password', message='Senhas não conferem.')
    ])    
    submit = SubmitField('Registrar') 
   

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():            
            raise ValidationError("Usuário já registrado.")
            


        
class LoginForm(FlaskForm):
    username = StringField('User', validators=[
        DataRequired()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    submit = SubmitField('Login')
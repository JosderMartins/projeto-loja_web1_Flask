from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, SelectField,\
    TextAreaField
from wtforms.validators import DataRequired, Length, Email
from wtforms.fields.html5 import EmailField, DateField
from wtforms.fields import FileField

from app.models import Role, User


class NameForm(FlaskForm):
    name = StringField('Qual o seu nome?', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class PostForm(FlaskForm):
    body = TextAreaField(
        'O que você está pensando?',
        validators=[DataRequired()]
    )
    submit = SubmitField('Enviar')

class ProdForm(FlaskForm):
    prod_nome = StringField('Nome produto', validators=[
        Length(1, 64)
    ])
    prod_classe = StringField('Classe de produto', validators=[
        Length(1, 64)
    ])
    prod_autor = StringField('Autor/Distribuidora', validators=[
        Length(1, 64)
    ])
    prod_preco = StringField('Preço', validators=[
        Length(1, 20)
    ])
    prod_estoque = StringField('Estoque', validators=[
        Length(1, 20)
    ])
    prod_arquivo = StringField('Inserir nome.extensão do arquivo que esta na pasta img, Exemplo: ( livro5.jpg )', validators=[
        Length(1,64)
    ])
    prod_imagem = FileField('Upload de imagem do produto, Obs.: não funcionando')    
    submit = SubmitField('Enviar')

    #def validate_image(self, field):
        # field.data:
        #    field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)


class EditProfileForm(FlaskForm):
    name = StringField('Nome completo', validators=[
        Length(1, 64)
    ])
    nascimento = DateField('Data de nascimento', validators=[
        DataRequired()
    ])
    email = EmailField('Email', validators=[
        DataRequired(), Length(1,64)
    ])
    cidade = StringField('Cidade de residência', validators=[
        DataRequired(), Length(1,60)
    ])
    about_me = TextAreaField('Sobre mim')
    submit = SubmitField('Enviar')


class EditProfileAdminForm(FlaskForm):
    username = StringField('Usuário', validators=[
        DataRequired(), Length(1, 64)
    ])
    nascimento = DateField('Data de nascimento', validators=[
        DataRequired()
    ])
    email = EmailField('Email', validators=[
        DataRequired(), Length(1,64)
    ])
    cidade = StringField('Cidade de residência', validators=[
        DataRequired(), Length(1,60)
    ])
    role = SelectField('Função', coerce=int)
    name = StringField('Nome completo', validators=[
        Length(1, 64)
    ])
    about_me = TextAreaField('Sobre mim')
    submit = SubmitField('Enviar')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [
            (role.id, role.name)
            for role in Role.query.order_by(Role.name).all()
        ]
        self.user = user

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Usuário já existe!')

class RoleForm(FlaskForm):
    name = StringField('Função', validators=[
        DataRequired()
    ])
    submit = SubmitField('Cadastrar')

    def validate_name(self, field):
        role = Role.query.filter_by(name=field.data).first()
        if role:
            raise ValidationError('Função já cadastrada')

from flask import flash, redirect, render_template, session, url_for, request
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from app import db
from app.decorators import admin_required, permission_required
from app.main.forms import (
    EditProfileAdminForm, EditProfileForm, NameForm, RoleForm, PostForm, ProdForm
)
from app.models import Role, User, Permission, Post, Produto

from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Parece que você alterou o nome!')
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'))

@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@main.route('/user/list', methods=['GET', 'POST'])
@login_required
def list_user():
    users = User.query.all()
    return render_template('list_user.html', users=users)


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return 'User invalid'
    follows = user.followers.all()
    return render_template('followers.html', username=username, followers=follows)

@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid User')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('Você já está seguindo esse usuário')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('Agora você já está seguindo esse usuário')
    return redirect(url_for('.user', username=username))

@main.route('/role/add', methods=['GET', 'POST'])
@login_required
def add_role():
    form = RoleForm()
    roles = Role.query.all()
    if form.validate_on_submit():
        new_role = Role()
        new_role.name = form.name.data
        db.session.add(new_role)
        db.session.commit()

        flash('Função cadastrada com sucesso.')
        return redirect(url_for('main.index'))
    return render_template('add_role.html', form=form, roles=roles)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.about_me = form.about_me.data
        current_user.email = form.email.data
        current_user.nascimento = form.nascimento.data
        current_user.cidade = form.cidade.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Perfil editado com sucesso!')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.about_me.data = current_user.about_me
    form.email.data = current_user.email
    form.nascimento.data = current_user.nascimento
    form.cidade.data = current_user.cidade
    return render_template(
        'edit-profile.html', form=form, username=current_user.username)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.about_me = form.about_me.data
        user.email = form.email.data
        user.nascimento = form.nascimento.data
        user.cidade = form.cidade.data
        db.session.add(user)
        db.session.commit()
        flash('Usuário editado pelo administrador com sucesso!')
        return redirect(url_for('.user', username=user.username))
    form.username.data = user.username
    form.role.data = user.role_id
    form.name.data = user.name
    form.about_me.data = user.about_me
    form.email.data = user.email
    form.nascimento.data = user.nascimento
    form.cidade.data = user.cidade
    return render_template(
        'edit-profile.html', form=form, username=user.username
    )

@main.route('/produtos')
def produtos():
    produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos)

@main.route('/detalhes_produto/<int:id>')
def produto_detalhado(id):
    produto = Produto.query.filter_by(id=id).first_or_404()
    return render_template('produto_detalhado.html', produto=produto)

@main.route('/mais_vendidos')
def mais_vendidos():
    return render_template('maisvendidos.html')

@main.route('/sobre')
def sobre():
    return render_template('sobre.html')

@main.route('/contato', methods=['GET','POST'])
def contato():
    return render_template('contato.html')

@main.route('/posts', methods=['GET','POST'])
def posts():
    form = PostForm()
    if current_user.has_permission(Permission.WRITE) and form.validate_on_submit():
        post = Post(
            body=form.body.data, author=current_user._get_current_object()
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(
        Post.timestamp.desc()
    ).paginate(
        page, per_page=10, error_out=False  
    )
    posts = pagination.items
    return render_template('posts.html', form=form, posts=posts , pagination=pagination)

@main.route('/cadastro_produtos/', methods=['GET', 'POST'])
@login_required
@admin_required
def cadastro_prod():
    form = ProdForm()
    if form.validate_on_submit():
        produto = Produto(
            prod_nome=form.prod_nome.data,
            prod_classe=form.prod_classe.data,
            prod_autor=form.prod_autor.data,
            prod_preco=form.prod_preco.data,
            prod_estoque=form.prod_estoque.data,
            #prod_imagem=form.prod_imagem.data,
            prod_arquivo=form.prod_arquivo.data          
        )
        db.session.add(produto)
        db.session.commit()
        flash('Produto cadastrado')
        return redirect('/cadastro_produtos')
    return render_template('/registro_produtos.html', form=form)

@main.route('/deletar_produtos/', methods=['GET', 'POST'])
@login_required
@admin_required
def deletar_prod():
    form = ProdForm()
    if form.validate_on_submit():
        produto = Produto(
            prod_nome=form.produto.id           
        )
        db.session.delete(produto)
        db.session.commit()
        flash('Produto cadastrado')
        return redirect('/cadastro_produtos')
    return render_template('/deletar_produtos.html', form=form)
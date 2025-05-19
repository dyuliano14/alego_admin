from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from .forms import LoginForm, RecuperarSenhaForm, RedefinirSenhaForm  # <- esses dois novos
from .forms import RegisterForm
from werkzeug.security import generate_password_hash
from . import db
from flask_mail import Message, Mail
from .utils import gerar_token, verificar_token
import os
import csv
import json

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Credenciais inválidas', 'danger')

    return render_template('admin/login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')

@main.route('/nova_disciplina', methods=['GET', 'POST'])
@login_required
def nova_disciplina():
    if request.method == 'POST':
        nome = request.form.get('nome_disciplina').strip().lower()
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], nome)
        os.makedirs(path, exist_ok=True)

        modelos = {
            'index.html': '<h2>{{ nome }}</h2><p>Bem-vindo!</p>',
            'aulas.html': '<section class="aula_pdf"><h2>Aulas</h2></section>',
            'planejamento.html': '<section class="planejamento"><h2>Planejamento</h2></section>',
            'resumos.html': '<section class="resumos"><h2>Resumos</h2></section>',
            'flashcards.html': '<section id="flashcard-container"><h2>Flashcards</h2></section>',
            'apresentacoes.html': '<section class="apresentacoes"><h2>Apresentações</h2></section>'
        }

        for nome_arquivo, conteudo in modelos.items():
            with open(os.path.join(path, nome_arquivo), 'w', encoding='utf-8') as f:
                f.write(conteudo.replace('{{ nome }}', nome.capitalize()))

        flash(f'Disciplina "{nome}" criada com sucesso!')
        return redirect(url_for('main.dashboard'))

    return render_template('admin/nova_disciplina.html')

@main.route('/disciplinas/<nome>/upload_flashcards', methods=['POST'])
@login_required
def upload_flashcards(nome):
    file = request.files.get('file')
    if not file or not file.filename.endswith('.csv'):
        flash("Envie um arquivo .CSV válido.")
        return redirect(url_for('main.dashboard'))

    path = os.path.join(current_app.config['UPLOAD_FOLDER'], nome)
    os.makedirs(path, exist_ok=True)

    reader = csv.DictReader(file.stream.read().decode('utf-8').splitlines())
    data = list(reader)

    json_path = os.path.join(path, 'flashcards.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    flash("Flashcards enviados com sucesso!")
    return redirect(url_for('main.dashboard'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(username=form.username.data).first()
        if existing:
            flash('Usuário já existe!', 'danger')
            return redirect(url_for('main.register'))

        new_user = User(
            username=form.username.data,
            password=generate_password_hash(form.password.data)
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Usuário registrado com sucesso!', 'success')
        return redirect(url_for('main.login'))
    return render_template('admin/register.html', form=form)

mail = Mail()

@main.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = gerar_token(user.email)
            link = url_for('main.redefinir', token=token, _external=True)
            msg = Message('Recuperação de Senha ALEGO',
                          sender='seuemail@gmail.com',
                          recipients=[user.email])
            msg.body = f'Acesse este link para redefinir sua senha: {link}'
            mail.send(msg)
        flash('Se o e-mail estiver registrado, enviaremos um link.', 'info')
        return redirect(url_for('main.login'))
    return render_template('admin/recuperar.html', form=form)


@main.route('/redefinir/<token>', methods=['GET', 'POST'])
def redefinir(token):
    email = verificar_token(token)
    if not email:
        flash('Token inválido ou expirado', 'danger')
        return redirect(url_for('main.recuperar'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        user.password = form.password.data
        db.session.commit()
        flash('Senha redefinida com sucesso!', 'success')
        return redirect(url_for('main.login'))

    return render_template('admin/redefinir.html', form=form)
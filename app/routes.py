from flask import render_template, redirect, url_for, flash
from . import db
from .forms import LoginForm
from flask import current_app as app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Lógica de autenticação aqui
        flash('Login realizado com sucesso!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

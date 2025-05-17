from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
import os
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/disciplinas/<nome>/editar')
def editar_disciplina(nome):
    return render_template('editar_disciplina.html', nome=nome)

@main.route('/disciplinas/<nome>/upload', methods=['POST'])
def upload_html(nome):
    if 'arquivo' not in request.files:
        flash('Arquivo não encontrado.')
        return redirect(url_for('main.editar_disciplina', nome=nome))

    arquivo = request.files['arquivo']
    if arquivo.filename == '':
        flash('Nome de arquivo vazio.')
        return redirect(url_for('main.editar_disciplina', nome=nome))

    if not arquivo.filename.endswith('.html'):
        flash('Somente arquivos .html são aceitos.')
        return redirect(url_for('main.editar_disciplina', nome=nome))

    filename = secure_filename(arquivo.filename)
    caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], nome, filename)
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    arquivo.save(caminho)

    flash(f'{filename} enviado com sucesso!')
    return redirect(url_for('main.editar_disciplina', nome=nome))

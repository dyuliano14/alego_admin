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

import csv
import json

@main.route('/disciplinas/<nome>/upload_flashcards', methods=['POST'])
def upload_flashcards(nome):
    file = request.files.get('file')
    if not file or not file.filename.endswith('.csv'):
        flash("Envie um arquivo .CSV válido.")
        return redirect(url_for('main.editar_disciplina', nome=nome))

    disciplina_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], nome)
    os.makedirs(disciplina_dir, exist_ok=True)

    # Lê e converte o CSV
    csv_reader = csv.DictReader(file.stream.read().decode('utf-8').splitlines())
    flashcards = list(csv_reader)

    # Salva como JSON
    json_path = os.path.join(disciplina_dir, 'flashcards.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(flashcards, f, ensure_ascii=False, indent=2)

    flash("Flashcards enviados com sucesso!")
    return redirect(url_for('main.editar_disciplina', nome=nome))

@main.route('/')
def index():
    disciplinas = os.listdir(current_app.config['UPLOAD_FOLDER'])
    return render_template('home.html', disciplinas=disciplinas)



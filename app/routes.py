from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
import os
from werkzeug.utils import secure_filename
import csv
import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    disciplinas = os.listdir(current_app.config['UPLOAD_FOLDER'])
    return render_template('index.html', disciplinas=disciplinas)

@main.route('/nova_disciplina', methods=['GET', 'POST'])
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
        return redirect(url_for('main.index'))

    return render_template('nova_disciplina.html')

@main.route('/disciplinas/<nome>/editar')
def editar_disciplina(nome):
    return render_template('dashboard.html', nome=nome)

@main.route('/disciplinas/<nome>/upload_flashcards', methods=['POST'])
def upload_flashcards(nome):
    file = request.files.get('file')
    if not file or not file.filename.endswith('.csv'):
        flash("Envie um arquivo .CSV válido.")
        return redirect(url_for('main.editar_disciplina', nome=nome))

    path = os.path.join(current_app.config['UPLOAD_FOLDER'], nome)
    os.makedirs(path, exist_ok=True)

    reader = csv.DictReader(file.stream.read().decode('utf-8').splitlines())
    data = list(reader)

    json_path = os.path.join(path, 'flashcards.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    flash("Flashcards enviados com sucesso!")
    return redirect(url_for('main.editar_disciplina', nome=nome))

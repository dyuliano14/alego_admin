from flask import Blueprint, jsonify, request, abort
from .models import Disciplina
from . import db
from flask import current_app

api = Blueprint('api', __name__)

# ❌ DESATIVA CSRF para todas as rotas da API
@api.before_request
def skip_csrf_for_api():
    if request.path.startswith('/api/') and request.method in ['POST', 'PUT', 'DELETE']:
        setattr(request, '_dont_enforce_csrf', True)


@api.route('/api/disciplinas', methods=['GET'])
def get_disciplinas():
    disciplinas = Disciplina.query.all()
    return jsonify([
    {
        'id': d.id,
        'titulo': d.titulo,
        'categoria': d.categoria,
        'tipo': d.tipo,
        'ordem': d.ordem,
        'descricao': d.descricao,
        'link': d.link
    } for d in disciplinas
])



@api.route('/api/disciplinas/<int:id>', methods=['GET'])
def get_disciplina(id):
    d = Disciplina.query.get_or_404(id)
    return jsonify({
        'id': d.id,
        'titulo': d.titulo,
        'categoria': d.categoria,
        'tipo': d.tipo,
        'ordem': d.ordem,
        'descricao': d.descricao,
        'link': d.link
    })


@api.route('/api/disciplinas', methods=['POST'])
def criar_disciplina():
    data = request.get_json()
    nova = Disciplina(
        titulo=data.get('titulo'),
        categoria=data.get('categoria'),
        tipo=data.get('tipo'),
        ordem=data.get('ordem', 0),
        descricao=data.get('descricao'),
        link=data.get('link')
    )
    db.session.add(nova)
    db.session.commit()
    return jsonify({'message': 'Disciplina criada com sucesso!'}), 201


@api.route('/api/disciplinas/<int:id>', methods=['PUT'])
def atualizar_disciplina(id):
    d = Disciplina.query.get_or_404(id)
    data = request.get_json()
    d.titulo = data.get('titulo', d.titulo)
    d.categoria = data.get('categoria', d.categoria)
    d.tipo = data.get('tipo', d.tipo)
    d.ordem = data.get('ordem', d.ordem)
    d.descricao = data.get('descricao', d.descricao)
    d.link = data.get('link', d.link)
    db.session.commit()
    return jsonify({'message': 'Disciplina atualizada com sucesso!'})


@api.route('/api/disciplinas/<int:id>', methods=['DELETE'])
def deletar_disciplina(id):
    d = Disciplina.query.get_or_404(id)
    db.session.delete(d)
    db.session.commit()
    return jsonify({'message': 'Disciplina removida com sucesso!'})

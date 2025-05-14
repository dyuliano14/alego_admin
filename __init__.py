from flask import Flask

app = Flask(__name__)

# Importe as rotas APENAS quando a aplicação estiver inicializada
# Isso é feito importando o módulo 'routes' no final do arquivo __init__.py
from . import routes
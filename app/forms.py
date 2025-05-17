from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class DisciplinaForm(FlaskForm):
    nome_disciplina = StringField('Nome da Disciplina', validators=[DataRequired()])
    submit = SubmitField('Criar')

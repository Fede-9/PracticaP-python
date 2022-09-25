# Libreria para trabajar con formularios
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class TareaForm(FlaskForm):
    tarea = StringField('Tarea:', validators=[DataRequired()])
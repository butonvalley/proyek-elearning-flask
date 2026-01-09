from flask_wtf import FlaskForm
from wtforms import DateTimeField, FileField, StringField, SubmitField,SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, Length

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired

class MateriForm(FlaskForm):
    judul = StringField("Judul Materi", validators=[DataRequired()])
    deskripsi = TextAreaField("Deskripsi")
    link_eksternal = StringField("Link eksternal")
    file = FileField("Upload File Materi")
    submit = SubmitField("Upload Materi")

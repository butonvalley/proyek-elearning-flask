from flask_wtf import FlaskForm
from wtforms import DateTimeField, FileField, StringField, SubmitField,SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, Length


class TugasForm(FlaskForm):
    judul = StringField("Judul Tugas", validators=[DataRequired()])
    deskripsi = TextAreaField("Deskripsi")
    file_tugas = FileField(
        "File Tugas"
    )
    deadline = DateTimeField("Deadline (Format: d-m-Y H:M)", format="%d-%m-%Y %H:%M")
    submit = SubmitField("Upload Tugas")

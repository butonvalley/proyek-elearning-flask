from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class MataKuliahForm(FlaskForm):
    kode = StringField(
        "Kode Mata Kuliah",
        validators=[
            DataRequired(message="Kode wajib diisi"),
            Length(min=3, max=10)
        ]
    )

    nama = StringField(
        "Nama Mata Kuliah",
        validators=[
            DataRequired(message="Nama mata kuliah wajib diisi"),
            Length(min=3, max=100)
        ]
    )

    sks = IntegerField(
        "SKS",
        validators=[
            DataRequired(message="SKS wajib diisi"),
            NumberRange(min=1, max=6)
        ]
    )

    submit = SubmitField("Simpan Mata Kuliah")

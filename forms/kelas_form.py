from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField,IntegerField
from wtforms.validators import DataRequired, Length

class KelasForm(FlaskForm):
    nama = StringField(
        "Nama Kelas",
        validators=[
            DataRequired(message="Nama kelas wajib diisi"),
            Length(min=3, max=50)
        ]
    )

    semester = SelectField(
        "Semester",
        choices=[
            ("Ganjil", "Ganjil"),
            ("Genap", "Genap")
        ],
        validators=[DataRequired()]
    )

    tahun_ajaran = StringField(
        "Tahun Ajaran",
        validators=[
            DataRequired(message="Tahun ajaran wajib diisi"),
            Length(min=9, max=20)
        ],
        description="Contoh: 2024/2025"
    )

    matakuliah_id = SelectField(
        "Mata Kuliah",
        coerce=str,
        validators=[DataRequired()]
    )

    submit = SubmitField("Simpan Kelas")

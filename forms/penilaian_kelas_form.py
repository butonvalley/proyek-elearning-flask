from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired

class PenilaianKelasForm(FlaskForm):
    nilai_a_min = FloatField("Nilai Minimal A", validators=[DataRequired()])
    nilai_b_min = FloatField("Nilai Minimal B", validators=[DataRequired()])
    nilai_c_min = FloatField("Nilai Minimal C", validators=[DataRequired()])
    nilai_d_min = FloatField("Nilai Minimal D", validators=[DataRequired()])
    nilai_e_min = FloatField("Nilai Minimal E", default=0)

    submit = SubmitField("Simpan Penilaian")

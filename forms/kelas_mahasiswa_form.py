from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

class KelasMahasiswaForm(FlaskForm):
    #update selanjutnya tambahkan dengan item lainnya
    nilai_akhir = FloatField(
        "Nilai Kumulatif",
        validators=[
            Optional(),
            NumberRange(min=0, max=100, message="Nilai harus 0–100")
        ]
    )
    
    submit = SubmitField("Update Kelas Mahasiswa")
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectMultipleField
from wtforms.validators import DataRequired, Length

class DosenForm(FlaskForm):
    nidn = StringField(
        "NIDN",
        validators=[DataRequired(), Length(min=5, max=20)]
    )
   
    submit = SubmitField("Simpan Dosen")

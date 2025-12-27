from flask_wtf import FlaskForm
from wtforms import DateTimeField, FileField, StringField, SubmitField,SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, Length


class TugasMahasiswaForm(FlaskForm):
    file_jawaban = FileField(
        "Upload Jawaban",
        validators=[
            DataRequired(),
        ]
    )
    submit = SubmitField("Kumpulkan")

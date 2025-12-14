from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class MahasiswaForm(FlaskForm):   
    nim = StringField("NIM", validators=[DataRequired(), Length(min=3)])    
    alamat = StringField("Alamat")
    angkatan = IntegerField("Angkatan")  
    submit = SubmitField("Login")
from flask_wtf import FlaskForm
from wtforms import StringField,  PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class RegisterForm(FlaskForm):
    fullname = StringField("Nama Lengkap", validators=[DataRequired(), Length(min=3)])   
    email = StringField("Email", validators=[DataRequired(), Length(min=3)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Daftar")

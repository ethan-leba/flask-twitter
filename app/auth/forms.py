from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SignupForm(FlaskForm):
    username = StringField('username: ', validators=[DataRequired()])
    password = StringField('password: ', validators=[DataRequired()])
    sfsubmit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('username: ', validators=[DataRequired()])
    password = StringField('password: ', validators=[DataRequired()])
    lfsubmit = SubmitField('Submit')

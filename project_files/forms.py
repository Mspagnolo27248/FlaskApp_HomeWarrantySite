#Flask_Auth/project_files/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError

from project_files.models import User




#Forms
class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('Username',validators=[DataRequired()])
    address = StringField('Address',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('Email has been registered')
    
    def validate_username(self, username):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError('Username has been registered')


class AddTicketForm(FlaskForm):
    #home_id = StringField('Owner Id') #Change to pass throough html.
    desc = TextAreaField('Describe Issue')
    createdate = StringField("Create Date")
    closedate = StringField("Close")    
    category = SelectField("Category",choices=[])
    submit = SubmitField('Submit')


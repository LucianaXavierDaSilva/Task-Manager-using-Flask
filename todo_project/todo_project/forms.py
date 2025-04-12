from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from flask_login import current_user

from .models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=10)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=10)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UpdateUserInfoForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=10)])
    submit = SubmitField('Update Info')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists.')


class UpdateUserPassword(FlaskForm):
    old_password = PasswordField('Enter Old Password', validators=[DataRequired()])
    new_password = PasswordField('Enter New Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')


class TaskForm(FlaskForm):
    task_name = StringField('Task Description', validators=[DataRequired()])
    submit = SubmitField('Add Task')


class UpdateTaskForm(FlaskForm):
    task_name = StringField('Update Task Description', validators=[DataRequired()])
    submit = SubmitField('Save Changes')

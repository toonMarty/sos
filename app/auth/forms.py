from app.models.user import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class LoginForm(FlaskForm):
    """
    Define a Login form
    """
    email = StringField('Email', validators=[DataRequired(),
                                             Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    login = SubmitField('Login')


class RegistrationForm(FlaskForm):
    """
    Define a Registration Form
    """
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),
                                             Length(1, 64), Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 128),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, '
               'numbers, dots, or underscores')
    ])

    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('confirm_password',
                                message='Passwords do not match')
    ])

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    sign_up = SubmitField('Sign Up')

    def validate_email(self, field):
        """
        Check that emails are unique
        Args:
            field: email value to check against existing value in database
        """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exists')

    def validate_username(self, field):
        """
        Check that usernames are unique
        Args:
            field: username to check against existing username in database
        """
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('username already exists. Please choose another username')


class ChangePasswordForm(FlaskForm):
    """
    Define how a user can change/update their password
    """
    current_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('confirm_password',
                                message='Passwords do not match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    change_password = SubmitField('Reset Password')


class PasswordResetRequestForm(FlaskForm):
    """
    Define a password reset Request form
    """
    user_email = StringField('Email', validators=[
        DataRequired(), Length(1, 64), Email()])

    reset_email_submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    """
    Define a password reset form
    """
    new_password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('confirm_password',
                                message="Passwords don't match")])

    confirm_password = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')


class ChangeEmailForm(FlaskForm):
    """
    Define change email form
    """
    new_email = StringField('New Email', validators=[
        DataRequired(), Length(1, 64), Email()])

    change_email_password = PasswordField('Password', validators=[DataRequired()])
    update_email = SubmitField('Change email address')

    def validate_email(self, field):
        """
        Check whether the email entered exists in the database
        Args:
            field: the input value to check against in the database
        """
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already exists. Please enter another email')


#!/usr/bin/env python3
from flask import request
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextAreaField, SelectField,
                     PasswordField, BooleanField, ValidationError)
from wtforms.validators import DataRequired, Length, Email, Regexp

from app.models.role import Role
from app.models.user import User


class TicketForm(FlaskForm):
    """
    Define a ticket form that the novice user will use to submit
    tickets
    """

    ticket_owner = StringField('Ticket owner', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    ticket_priority = SelectField('Priority', validators=[DataRequired()],
                                  choices=[('L', 'Low'), ('M', 'Medium'), ('H', 'High')])

    tv_session_password = PasswordField('Passcode', validators=[DataRequired()])
    team_viewer_id = StringField('TeamViewer ID', validators=[DataRequired()])

    issue = TextAreaField('Issue', validators=[DataRequired()],
                          render_kw={'placeholder': 'Describe your issue'})

    submit_ticket = SubmitField('Create')


class SearchForm(FlaskForm):
    q = StringField('Search Tickets', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'meta' not in kwargs:
            kwargs['meta'] = {'csrf': False}
        super(SearchForm, self).__init__(*args, **kwargs)


class EditUserProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Length(1, 64), Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must '
                                              'have only letters, numbers, '
                                              'dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    first_name = StringField('First name', validators=[Length(0, 32)])
    last_name = StringField('Last name', validators=[Length(0, 32)])
    department = StringField('Department', validators=[Length(0, 32)])
    edit_user = SubmitField('Update')

    def __init__(self, user, *args, **kwargs):
        super(EditUserProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if (field.data != self.user.email and
                User.query.filter_by(email=field.data).first()):
            raise ValidationError('Email already exists')

    def validate_username(self, field):
        if (field.data != self.user.username and
                User.query.filter_by(username=field.data).first()):
            raise ValidationError('Username already exists')



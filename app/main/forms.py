#!/usr/bin/env python3
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, PasswordField
from wtforms.validators import DataRequired


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
    team_viewer_id = StringField('Your ID', validators=[DataRequired()])

    issue = TextAreaField('Issue', validators=[DataRequired()],
                          render_kw={'placeholder': 'Describe your issue'})

    submit_ticket = SubmitField('Create')
    cancel_ticket = SubmitField('Cancel')


class SearchForm(FlaskForm):
    q = StringField('Search Tickets', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'meta' not in kwargs:
            kwargs['meta'] = {'csrf': False}
        super(SearchForm, self).__init__(*args, **kwargs)class SearchForm(FlaskForm):
    q = StringField('Search Tickets', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'meta' not in kwargs:
            kwargs['meta'] = {'csrf': False}
        super(SearchForm, self).__init__(*args, **kwargs)

#!/usr/bin/env python3
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, PasswordField
from wtforms.validators import DataRequired


class TicketForm(FlaskForm):
    ticket_owner = StringField('Ticket owner', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    ticket_priority = SelectField('Priority', validators=[DataRequired()],
                                  choices=[('L', 'Low'), ('M', 'Medium'), ('H', 'High')])
    tv_session_password = PasswordField('Passcode', validators=[DataRequired()])

    issue = TextAreaField('Issue', validators=[DataRequired()],
                          render_kw={'placeholder': 'Describe your issue'})

    submit_ticket = SubmitField('Create')
    cancel_ticket = SubmitField('Cancel')

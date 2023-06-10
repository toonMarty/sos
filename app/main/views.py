#!/usr/bin/env python3
"""
Code to run for each URL requested by the user
"""
from sqlalchemy import func

from app.main import main
from flask import render_template, redirect, url_for, flash, request
from app.main.forms import TicketForm
from app.models.ticket import Ticket
from app import db


@main.route('/', methods=['GET', 'POST'], strict_slashes=False)
def index():
    return render_template('index.html')


@main.route('/create-ticket', methods=['GET', 'POST'], strict_slashes=False)
def submit_ticket():
    form = TicketForm()

    if form.validate_on_submit():
        ticket = Ticket(ticket_owner=form.ticket_owner.data,
                        subject=form.subject.data,
                        ticket_priority=form.ticket_priority.data,
                        team_viewer_session_password=form.tv_session_password.data,
                        issue_description=form.issue.data)
        ticket.create_ticket()
        flash('Your ticket has been sent. Please Wait while an '
              'Agent resolves your issue')
        return redirect(url_for('main.index'))
    return render_template('create_ticket.html', form=form)


@main.route('/view-tickets', methods=['GET', 'POST'], strict_slashes=False)
def view_ticket():
    tickets = Ticket.query.order_by(Ticket.date_submitted.desc()).all()
    tkt_count = Ticket.ticket_count(tickets)
    
    return render_template('view_ticket.html', tickets=tickets, 
                           tkt_count=tkt_count)


@main.route('/view-tickets/<ticket_subject>', methods=['GET', 'POST'], 
            strict_slashes=False)
def view_ticket_by_subject(ticket_subject):
    tickets = Ticket.query.filter(Ticket.subject == ticket_subject).all()

    return render_template('specific_ticket.html', tickets=tickets, 
                           ticket_subject=ticket_subject)

#!/usr/bin/env python3
"""
Code to run for each URL requested by the user
"""
from sqlalchemy import func

from app.main import main
from flask import render_template, redirect, url_for, flash, request
from app.main.forms import TicketForm, SearchForm
from app.models.ticket import Ticket
from sqlalchemy.exc import OperationalError
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
    tickets = Ticket.query.group_by(Ticket.subject).order_by(Ticket.date_submitted.desc()).all()
    tkt_count = Ticket.ticket_count(tickets)
    
    return render_template('view_ticket.html', tickets=tickets, 
                           tkt_count=tkt_count)


@main.route('/view-tickets/<ticket_subject>', methods=['GET', 'POST'], 
            strict_slashes=False)
def view_ticket_by_subject(ticket_subject):
    tickets = Ticket.query.filter(Ticket.subject == ticket_subject).all()

    return render_template('specific_ticket.html', tickets=tickets, 
                           ticket_subject=ticket_subject)


@main.route('/agent/solve-tickets', methods=['GET', 'POST'], strict_slashes=False)
def solve_tickets():
    tickets = Ticket.query.order_by(Ticket.ticket_priority.asc()).all()
    tkt_count = Ticket.ticket_count(tickets)
    
    return render_template('solve_ticket.html', tickets=tickets,
                           tkt_count=tkt_count)

@main.before_request
def before_request():
    g.search_form = SearchForm()


@main.route('/search')
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.view_ticket'))

    try:
        page = request.args.get('page', 1, type=int)
        tickets, total = Ticket.search(g.search_form.q.data, page,
                                       current_app.config['TICKETS_PER_PAGE'])

        next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
            if page > page * current_app.config['TICKETS_PER_PAGE'] else None

        prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) if page > 1 else None

        return render_template('search.html', title='Search Tickets',
                               tickets=tickets,
                               next_url=next_url,
                               prev_url=prev_url)
    except OperationalError:
        return render_template('404.html')

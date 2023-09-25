#!/usr/bin/env python3
"""
Code to run for each URL requested by the user
"""
from flask_login import current_user
from sqlalchemy import func

from app.main import main
from app.decorators import permission_required, admin_required
from flask import render_template, redirect, url_for, flash, request, \
    session, g, current_app, abort
from app.main.forms import TicketForm, SearchForm
from app.models.ticket import Ticket
from sqlalchemy.exc import OperationalError
from app import db
from app.models.role import Permission
from app.models.user import User


@main.route('/', methods=['GET', 'POST'], strict_slashes=False)
def index():
    return render_template('index.html')


@main.route('/create-ticket', methods=['GET', 'POST'], strict_slashes=False)
@permission_required(Permission.CREATE_TICKET)
def submit_ticket():
    form = TicketForm()

    if current_user.can(Permission.CREATE_TICKET) and form.validate_on_submit():
        ticket = Ticket(ticket_owner=form.ticket_owner.data,
                        subject=form.subject.data,
                        ticket_priority=form.ticket_priority.data,
                        team_viewer_session_password=form.tv_session_password.data,
                        team_viewer_id=form.team_viewer_id.data,
                        issue_description=form.issue.data,
                        sender=current_user._get_current_object())
        ticket.create_ticket()
        flash('Your ticket has been sent. Please Wait while an '
              'Agent resolves your issue')
        return redirect(url_for('main.index'))
    return render_template('create_ticket.html', form=form)


@main.route('/view-tickets/<username>', methods=['GET', 'POST'], strict_slashes=False)
def view_ticket(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return render_template('404.html')
    # tickets = Ticket.query.group_by(Ticket.subject).order_by(Ticket.date_submitted.desc()).all()
    tickets = user.tickets.group_by(Ticket.subject).order_by(Ticket.date_submitted.desc()).all()
    tkt_count = Ticket.ticket_count(tickets)
    
    return render_template('view_ticket.html', user=user,
                           tickets=tickets, tkt_count=tkt_count)


@main.route('/view-tickets/<username>/<ticket_subject>', methods=['GET', 'POST'],
            strict_slashes=False)
def view_ticket_by_subject(username, ticket_subject):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return render_template('404.html')
    tickets = user.tickets.filter(Ticket.subject == ticket_subject).order_by(Ticket.date_submitted.desc()).all()
    # tickets = Ticket.query.filter(Ticket.subject == ticket_subject).all()

    return render_template('specific_ticket.html', username=username,
                           tickets=tickets, ticket_subject=ticket_subject)


@main.route('/agent/solve-tickets', methods=['GET', 'POST'], strict_slashes=False)
@permission_required(Permission.SOLVE)
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

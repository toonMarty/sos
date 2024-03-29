#!/usr/bin/env python3
"""
Code to run for each URL requested by the user
"""
from flask_login import current_user, login_required
from sqlalchemy import func

from app.main import main
from app.decorators import permission_required, admin_required
from flask import render_template, redirect, url_for, flash, request, \
    session, g, current_app, abort
from app.main.forms import TicketForm, SearchForm, EditUserProfileAdminForm
from app.models.ticket import Ticket
from sqlalchemy.exc import OperationalError
from app import db
from app.models.role import Permission, Role
from app.models.user import User
from app.ticket_allocator import allocate_ticket
from sqlalchemy import or_


@main.route('/', methods=['GET', 'POST'], strict_slashes=False)
def index():
    return render_template('index.html')


@main.route('/create-ticket', methods=['GET', 'POST'], strict_slashes=False)
@permission_required(Permission.CREATE_TICKET)
def submit_ticket():
    form = TicketForm()

    form.ticket_owner.data = current_user.username
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
@login_required
def view_ticket(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return render_template('404.html')
    if user.username != current_user.username:
        return render_template('403.html')
    # tickets = Ticket.query.group_by(Ticket.subject).order_by(Ticket.date_submitted.desc()).all()
    tickets = user.tickets.group_by(Ticket.subject).order_by(Ticket.date_submitted.desc()).all()
    tkt_count = user.tickets.count()
    
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


@main.route('/agent/<username>/solve-tickets', methods=['GET', 'POST'], strict_slashes=False)
@permission_required(Permission.SOLVE)
def solve_tickets(username):
    tickets = Ticket.query.order_by(Ticket.ticket_priority.asc()).all()  # returns a list of all ticket objects
    user = User.query.filter_by(username=username).first()
    users = User.query.filter_by(department='Testing').all()

    res = allocate_ticket(tickets, users)

    tickets = res[user]
    user.tickets = tickets
    tickets = user.tickets.order_by(Ticket.date_submitted.desc()).all()

    return render_template('solve_ticket.html', tickets=tickets, username=username)


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


@main.route('/user/<username>', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    if user.username != current_user.username and not current_user.can(Permission.ADMIN):
        return render_template('403.html')
    tkt_count = user.tickets.count()
    return render_template('user_profile.html', user=user, tkt_count=tkt_count)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditUserProfileAdminForm(user=user)

    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.department = form.department.data
        db.session.add(user)
        db.session.commit()
        flash(f"{user.username}'s profile successfully updated")
        return redirect(url_for('main.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.department.data = user.department

    return render_template('edit_profile_admin.html', form=form, user=user)


@main.route('/user/<username>/dashboard', methods=['GET', 'POST'], strict_slashes=False)
def user_dashboard(username):
    user = User.query.filter_by(username=username).first()
    sent = user.tickets.count()

    # bad bad idea
    tickets = Ticket.query.order_by(Ticket.ticket_priority.asc()).all()  # returns a list of all ticket objects
    user_agent = User.query.filter_by(username=username).first()
    users_agents = User.query.filter_by(department='Testing').all()

    res = allocate_ticket(tickets, users_agents)

    tickets = res[user_agent]
    user_agent.tickets = tickets
    new_tickets = user_agent.tickets.count()

    '''if user_agent:
        return render_template('solve_ticket.html', tickets=tickets)'''
    return render_template('user_dashboard.html', user=user,
                           sent=sent, new_tickets=new_tickets, tickets=tickets)



from flask import render_template, url_for, flash, request, redirect
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from .forms import (LoginForm, RegistrationForm, ChangePasswordForm,
                    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm)
from app.models.user import User
from app import db
from app.email import send_email


@auth.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """
    View that handles user login
        Validate form on submission
            Check if user exists in the database /load user from database
                If user exists and password checks out:
                    Record user as logged in for the user session
                    set next to the next query string url
                    if next query string is not available:
                        redirect user back to home page
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')

            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid email address or password')
    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['GET'], strict_slashes=False)
@login_required
def logout():
    """
    Log out a user
    """
    # remove and reset user session
    logout_user()
    flash('You have logged out successfully')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    """
    Handle new user registration
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            department=form.department.data,
            email=form.email.data,
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation message has been sent to your email')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.before_app_request
def before_request():
    """
    Allow an unconfirmed user to access
    authentication pages that will facilitate
    the user's confirmation
    """
    if (current_user.is_authenticated
            and not current_user.confirmed
            and request.blueprint != 'auth'
            and request.endpoint != 'static'):
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    """
    Confirm a user's account given a token
    Args:
        token: the token that will be used to confirm a user
        account request for a particular user
    """
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('Your account is now confirmed.')
    else:
        flash('The confirmation link is invalid or has expired')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    """
    Handle unconfirmed accounts
    """
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    """
    Handle resending of confirmation tokens
    """
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to your email')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """
    Handle user password updates
    """
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template('auth/change_password.html', form=form)


@auth.route('/reset-password', methods=['GET', 'POST'])
def password_reset_request():
    """
    Handle forgot password requests
    """
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.user_email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password', user=user, token=token)
        flash('An email with instructions to reset your password has been sent to you')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def password_reset(token):
    """
    Handle password resets using a token
    Args:
        token: the token that will be used to confirm a password
        reset request for a particular user
    """
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.new_password.data):
            db.session.commit()
            flash('Your password has been updated')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password_forgot.html', form=form)


@auth.route('/change-email', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def change_email_request():
    """
    Handle email change requests
    """
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.check_password(form.change_email_password.data):
            new_email = form.new_email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to '
                  'confirm your new email has been sent to you')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password')
    return render_template('auth/change_email.html', form=form)


@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been successfully updated')
    else:
        flash('Invalid request')
    return redirect(url_for('main.index'))





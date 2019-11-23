import os
import random
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from application.web_forms import RegistrationForm, LoginForm, AdminForm, GroupForm, ChangeAdminForm, UpdateAccountInfoForm, ChangePasswordForm
from flask_login import login_required, current_user, login_required
from .models import Group, Member, User, Paylist
import datetime
from datetime import date
from application import db
from sqlalchemy.sql import text
from sqlalchemy import create_engine

view = Blueprint('view', __name__)

engine = create_engine('postgresql://postgres:password@localhost/esusu', convert_unicode=True)
connection  = engine.connect()

@view.route('/')
@view.route('/home')
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        flash('you need to sign out to access that page')
        return redirect(url_for('view.account_home'))
    else:
        return render_template('login.html', form=form, title='Esusu-login')


@view.route('/signup')
def signup():

    form = RegistrationForm()
    if current_user.is_authenticated:
        flash('you need to sign out to access that page')
        return redirect(url_for('view.account_home'))
    else:
        return render_template('signup.html', form=form, title='Esusu-signup')

@view.route('/account_home')
@login_required
def account_home():
    groups = Group.query.all()

    return render_template('home.html', groups=groups)

@view.route('/account_profile')
@login_required
def account_profile():

    form = UpdateAccountInfoForm()
    form.username.data = current_user.username
    form.email.data = current_user.email
    profile_pix = url_for('static', filename=f'images/{current_user.profil_pix}')
    return render_template('account_home.html', form=form, current_user=current_user, profile_pix=profile_pix)

@view.route('/admin_signup')
@login_required
def admin_signup():

    form = AdminForm()
    return render_template('admin-signup.html', form=form,)

@view.route('/group_creation')
@login_required
def group_creation():

    form = GroupForm()

    return render_template('create-group-page.html', form=form)

@view.route('/group')
@login_required
def group():

    return render_template('group.html', current_user=current_user)


@view.route('/group_details')
@login_required
def group_details():

    group_id = request.args.get('group_id')

    group = Group.query.get(group_id)
    member = Member.query.filter_by(group_id=group_id).filter_by(user_id=current_user.id).first()
    not_member = connection.execute(
        text(f'select * from public.member full join public.user on public.member.user_id = public.user.id where public.member.group_id = {group.id}')
    )

    return render_template('group-details.html', group=group, current_user=current_user, group_id=group_id, member=member, not_member=not_member)


@view.route('/member')
@login_required
def member():

    group_id  = request.args.get('group_id')

    group = Group.query.get(group_id)
    members_in_group = Member.query.filter_by(group_id=group_id).all()

    if current_user.is_authenticated and current_user.is_admin:
        return render_template('member-detail.html', members_in_group=members_in_group, group=group, group_id=group_id)
    else:
        return abort(404)

@view.route('/busery')
@login_required
def busery():
    group_id  = request.args.get('group_id')
    group = Group.query.get(group_id)
    members_in_group = Member.query.filter_by(group_id=group_id).all()

    if current_user.is_authenticated and current_user.is_admin:
        return render_template('busery.html', group=group, members_in_group=members_in_group, group_id=group_id)
    else:
        return abort(404)


@view.route('/admin_pannel')
@login_required
def admin_pannel():
    form = ChangeAdminForm()
    group_id  = request.args.get('group_id')
    group = Group.query.get(group_id)
    paylist = Paylist.query.filter_by(group_id=group_id).first()

    if current_user.is_authenticated and current_user.is_admin:
        return render_template('admin-pannel.html', group=group, group_id=group_id, form=form, paylist=paylist)
    else:
        return abort(404)

@view.route('/payee_list')
@login_required
def payee_list():
    group_id = request.args.get('group_id')
    group = Group.query.get(group_id)
    member = Member.query.filter_by(group_id=group_id).all()
    paylist = Paylist.query.filter_by(group_id=group_id).first()

    if current_user.is_authenticated and current_user.is_admin:
        return render_template('payee-list.html', group_id=group_id, group=group, member=member, paylist=paylist)
    else:
        return abort(404)

@view.route('/reset_password')
def reset_password():

    form = ChangePasswordForm()

    return render_template('reset_pass.html', form=form)
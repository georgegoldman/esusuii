import random
from flask import Blueprint, render_template, request
from application.web_forms import RegistrationForm, LoginForm, AdminForm, GroupForm, ChangeAdminForm
from flask_login import login_required, current_user
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
def home():
    return render_template('home.html', title='esusu-home')


@view.route('/signup')
def signup():

    form = RegistrationForm()

    return render_template('signup.html', form=form, title='esusu-signup')


@view.route('/login')
def login():
    form = LoginForm()

    return render_template('login.html', form=form, title='esusu-login')

@view.route('/account_home')
@login_required
def account_home():

    member = Member.query.filter_by(user_id=current_user.id).all()
    return render_template('account_home.html', current_user=current_user, member=member)

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
    members = Member.query.all()
    groups = Group.query.all()
    return render_template('group.html', members=members, groups=groups)


@view.route('/member')
@login_required
def member():

    group_id  = request.args.get('group_id')

    group = Group.query.get(group_id)
    members_in_group = Member.query.filter_by(group_id=group_id).all()
    return render_template('member-detail.html', members_in_group=members_in_group, group=group, group_id=group_id)

@view.route('/busery')
@login_required
def busery():
    group_id  = request.args.get('group_id')
    group = Group.query.get(group_id)
    members_in_group = Member.query.filter_by(group_id=group_id).all()

    return render_template('busery.html', group=group, members_in_group=members_in_group, group_id=group_id)

@view.route('/group_details')
@login_required
def group_details():

    group_id = request.args.get('group_id')

    datas = connection.execute(
        text(f" select * from public.user inner join public.member on public.member.user_id = public.user.id  where public.member.group_id = {group_id}")
    )
    group = Group.query.filter_by(id=group_id).first()
    members_in_group = Member.query.filter_by(group_id=group.id).all()

    user = User.query.all()

    members = connection.execute(
        text(f"select * from  public.user full join public.member on public.user.id = public.member.user_id	")
    )

    return render_template('group-details.html', datas=datas, members=members, group=group, current_user=current_user, members_in_group=members_in_group, group_id=group_id)



@view.route('/admin_pannel')
@login_required
def admin_pannel():
    form = ChangeAdminForm()
    group_id  = request.args.get('group_id')
    group = Group.query.get(group_id)
    paylist = Paylist.query.filter_by(group_id=group_id).first()

    return render_template('admin-pannel.html', group=group, group_id=group_id, form=form, paylist=paylist)

@view.route('/payee_list')
@login_required
def payee_list():
    group_id = request.args.get('group_id')
    group = Group.query.get(group_id)
    member = Member.query.filter_by(group_id=group_id).all()
    paylist = Paylist.query.filter_by(group_id=group_id).first()
    return render_template('payee-list.html', group_id=group_id, group=group, member=member, paylist=paylist)

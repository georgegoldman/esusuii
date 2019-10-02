from flask import Blueprint, render_template, request
from application.web_forms import RegistrationForm, LoginForm, AdminForm, GroupForm, AdduserForm
from flask_login import login_required, current_user
from .models import Group, Member, User

view = Blueprint('view', __name__)


@view.route('/')
@view.route('/home')
def home():
    return render_template('home.html', title='eltd-home')


@view.route('/signup')
def signup():

    form = RegistrationForm()

    return render_template('signup.html', form=form, title='eltd-signup')


@view.route('/login')
def login():
    form = LoginForm()

    return render_template('login.html', form=form, title='eltd-login')

@view.route('/account_home')
@login_required
def account_home():


    return render_template('account_home.html', username=current_user.email)

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


    group  = Group.query.all()
    member = Member.query.all()



    return render_template('group.html', groups=group, member=member, count = 0, one = 1)


@view.route('/member')
@login_required
def add_member():

    form = AdduserForm()
    group_name = request.args.get('members')

    member = Member.query.all()
    group = Group.query.filter_by(group_name=group_name).first()

    return render_template('add-member.html', members=member, group_name=group_name, form=form, group=group)

@view.route('/group_details')
@login_required
def group_details():

    group_name = request.args.get('group_name')

    group = Group.query.filter_by(group_name=group_name).first()

    return render_template('group-details.html', group=group)

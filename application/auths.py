from flask import Blueprint, render_template, redirect, url_for, flash
from application.web_forms import RegistrationForm, LoginForm, AdminForm, GroupForm
from application.models import User, Group, Member
from application import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST'])
def signup():

    form = RegistrationForm()

    if form.validate_on_submit():
        password = form.password.data
        email = form.email.data

        user = User.query.filter_by(email=email).first()

        if user:
            flash('user already exist!')
            return render_template('signup.html', form=form)


        user = User(email=email, password=password)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('view.login'))
    flash('check your email if correct !')
    return redirect(url_for('view.signup'))


@auth.route('/login', methods=['POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user and user.password==password:
            login_user(user)
            return redirect(url_for('view.account_home'))

        else:
            flash(f"Account does not exit !")
            return redirect(url_for('view.login'))

@auth.route('/logout')
@login_required
def logout():

    logout_user()
    return redirect(url_for('view.home'))

'''admin creation and group route'''

@auth.route('/create_admin', methods=['POST'])
@login_required
def create_admin():

    form = AdminForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if current_user.email != email or current_user.password != password:
            flash('invalid logs')
            return redirect(url_for('view.admin_signup'))
        else:
            if current_user.is_admin == False:
                user.is_admin=True
                db.session.commit()
                flash('Your account have been upgraded to an administrative account')
                return redirect(url_for('view.group_creation'))
            elif user.is_admin == True:
                return redirect(url_for('view.group_creation'))
    return render_template('admin-signup.html', form=form)

'''create group logic'''

@auth.route('/create_group', methods=['POST'])
@login_required
def create_group():

    form = GroupForm()

    if form.validate_on_submit():
        group_name = form.group_name.data
        group_target = int(form.group_target.data)


        group = Group.query.filter_by(group_name=group_name).first()

        group = Group(group_name=group_name, group_admin=current_user.email, group_members=int(1), group_target=group_target, current_contribution=int(0), user_id=current_user.id)
        db.session.add(group)
        db.session.commit()

        paymt_calc = int(group.group_target)/group.group_members
        weekly_target = paymt_calc/4

        member = Member(member_name=current_user.email, group_name=group_name, weekly_target=weekly_target, monthly_target=paymt_calc, group_id=group.id)

        db.session.add(member)
        db.session.commit()


        return redirect(url_for('view.group'))

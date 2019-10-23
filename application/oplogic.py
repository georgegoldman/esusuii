from flask import Blueprint, flash, redirect, url_for, request, render_template, Markup
from flask_login import login_required, current_user
from .web_forms import AdminForm, GroupForm, ChangeAdminForm
from .models import User, Group, Member
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text
from sqlalchemy import create_engine

oplogic = Blueprint('oplogic', __name__)
engine = create_engine('postgresql://postgres:password@localhost/esusu', convert_unicode=True)
connection = engine.connect()

'''admin creation and group route'''

@oplogic.route('/create_admin', methods=['POST'])
@login_required
def create_admin():

    form = AdminForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if current_user.email != email or not check_password_hash(current_user.password, password):
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

@oplogic.route('/create_group', methods=['POST'])
@login_required
def create_group():

    form = GroupForm()

    if form.validate_on_submit():
        group_name = str(form.group_name.data)
        member_limit = int(form.member_limit.data)
        group_target = int(form.group_target.data)

        group = Group(group_name=group_name, group_admin=current_user.id, group_members=1, member_limit=member_limit, group_target=group_target, current_contribution=0, user_id=current_user.id)
        db.session.add(group)
        db.session.commit()

        group = Group.query.filter_by(group_name=group_name).first()

        weekly_target = (group_target/member_limit)/4
        monthly_target = group_target/member_limit
        member = Member(weekly_target=weekly_target, monthly_target=monthly_target, group_id=group.id, user_id=current_user.id)
        db.session.add(member)
        db.session.commit()

        current_user.group_in += 1
        db.session.commit()

        flash(f'{group.group_name} have been successfully created')
        return redirect(url_for('view.group'))

'''adding a member to a group '''
@oplogic.route('/join_group', methods=['GET','POST'])
@login_required
def join_group():
    group_id = request.args.get('group_id')
    member = Member.query.filter_by(group_id=group_id).filter_by(user_id=current_user.id).first()
    members_in_group = Member.query.filter_by(group_id=group_id).count()
    group = Group.query.get(group_id)

    if group.member_limit == members_in_group:
        flash(f'{group.group_name} has reached it limit')
        return render_template('account_home.html')
    else:
        if member:
            flash('You are already a member to this group')
            return render_template('account_home.html')
        else:
            weekly_target = (group.group_target/group.member_limit)/4
            monthly_target = group.group_target/group.member_limit
            new_member = Member(weekly_target=weekly_target,monthly_target=0,group_id=group_id,user_id=current_user.id)
            db.session.add(new_member)
            db.session.commit()

            current_user.group_in += 1
            db.session.commit()


            group.group_members += 1
            db.session.commit()

            flash('You have been added successfully.')
            return render_template('account_home.html')


#Remove a member route
@oplogic.route('/leave_group')
@login_required
def remove_user():
    group_id = request.args.get('group_id')
    member = Member.query.filter_by(group_id=group_id).filter_by(user_id=current_user.id).first()
    group = Group.query.get(group_id)

    if member:
        db.session.delete(member)
        db.session.commit()

        current_user.group_in -= 1
        db.session.commit()

        group = Group.query.get(group_id)
        group.group_members -= 1
        db.session.commit()

        flash(f'You have been removed successfully {group.group_name}.')
        return render_template('account_home.html')
    else:

        flash(f'You are not a member to this {group.group_name}')
        return render_template('account_home.html')

@oplogic.route('/start_tenure')
@login_required
def start_tenure():

    group_id  = rquest.args.get()
    member = Member.query.filter_by()
    return 'tenure started'

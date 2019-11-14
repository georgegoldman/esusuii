import os
import random
from random import shuffle
from flask import Blueprint, flash, redirect, url_for, request, render_template, Markup
from flask_login import login_required, current_user, login_required
from .web_forms import AdminForm, GroupForm, ChangeAdminForm
from .models import User, Group, Member, Paylist
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text
from sqlalchemy import create_engine

oplogic = Blueprint('oplogic', __name__)
engine = create_engine(os.environ.get('DATABASE_URL'), convert_unicode=True)
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
        target = (group_target/member_limit)/4


        group = Group(group_name=group_name, group_admin=current_user.id, group_members=1, member_limit=member_limit, member_target = target, group_target=group_target, current_contribution=0, user_id=current_user.id)
        db.session.add(group)
        db.session.commit()

        group = Group.query.filter_by(group_name=group_name).first()

        paylist = Paylist(group_id=group.id)
        db.session.add(paylist)
        db.session.commit()

        monthly_target = group_target/member_limit
        member = Member(member_target=target, monthly_target=monthly_target, group_id=group.id, user_id=current_user.id)
        db.session.add(member)
        db.session.commit()

        current_user.group_in += 1
        db.session.commit()

        flash(f'{group.group_name} have been successfully created')
        return redirect(url_for('view.group_creation'))

#join group
@oplogic.route('/join_group')
@login_required
def join_group():
    group_id = request.args.get('group_id')
    member = Member.query.filter_by(group_id=group_id).filter_by(user_id=current_user.id).first()
    members_in_group = Member.query.filter_by(group_id=group_id).count()
    group = Group.query.get(group_id)

    if group.member_limit == members_in_group:
        res = {
            'error' : '0',
            'message': f'{group.group_name} has reached it limit',
        }
        return res

    else:
        if member:
            res = {
                'error' : '0',
                'message': 'You are already a member to this group',
            }
            return res

        else:
            member_target = (group.group_target/group.member_limit)/4
            monthly_target = group.group_target/group.member_limit
            new_member = Member(username=current_user.username, member_target=member_target,monthly_target=monthly_target,group_id=group_id,user_id=current_user.id)
            db.session.add(new_member)
            db.session.commit()

            current_user.group_in += 1
            db.session.commit()


            group.group_members += 1
            db.session.commit()

            res = {
                'error' : '0',
                'message': f'{current_user.username} you have been successfully added to {group.group_name} Group',
            }

            return res


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

        res = {
            'error' : '0',
            'message' : f'{current_user.username} you have been successfully removed from this group                                    '
        }
        return res
    else:

        res = {
            'error' : '0',
            'message' : f'You are not a member to this {group.group_name}'
        }
        return res

@oplogic.route('/start_tenure')
@login_required
def start_tenure():

    group_id  = request.args.get('group_id')
    member = Member.query.filter_by(group_id=group_id).all()
    payee_list = Paylist.query.filter_by(group_id=group_id).first()
    users = User.query.all()
    paylist = list()

    shuffle(member)
    print(member)
    i = 0
    for y in member:
        for user in users:
            if y.user_id == user.id:
                i += 1
                #paylist.append(f'{i}.{user.username}')
                paylist.append(user.id)
                if len(member) == i:
                    #payee_listToStr = ' '.join([str(elem) for elem in payee_list])
                    payee_list.payee_list = paylist
                    payee_list.start_tenure = True
                    db.session.commit()

                    print(paylist)

    flash('tenure has started go to the go to payee list to see who takes the money first')
    return render_template('account_home.html')

@oplogic.route('/change_admin', methods=['GET', 'POST'])
@login_required
def change_admin():
    form  = ChangeAdminForm()
    group_id = request.args.get('group_id')
    if form.validate_on_submit:
        member_id = form.members_id.data
        member = Member.query.get(member_id)
        if int(member.group_id) == int(group_id):
            group = Group.query.get(group_id)
            if member.user_id == group.group_admin:
                flash(f"You are already the group administrator ")
                return render_template('account_home.html')
            group.group_admin = member.user_id
            group.user_id = member.user_id
            db.session.commit()
            flash(f"This user is now the administrator of this group ")
            return render_template('account_home.html')
        elif int(member.group_id) == None:
            flash(f"This user is not a member to this group ")
            return render_template('account_home.html')
        else:
            flash(f"This user is not a member to this group ")
            return render_template('account_home.html')

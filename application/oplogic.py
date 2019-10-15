from flask import Blueprint, flash, redirect, url_for, request, render_template, Markup
from flask_login import login_required, current_user
from .web_forms import AdminForm, GroupForm, AdduserForm, ChangeAdminForm
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
        group_target = int(form.group_target.data)

        user = User.query.filter_by(id=current_user.id).first()

        group = Group.query.filter_by(group_name=group_name).first()

        group = Group(group_name=group_name, group_admin=current_user.id, group_members=int(1), group_target=group_target, current_contribution=int(0), user_id=current_user.id)
        db.session.add(group)
        db.session.commit()

        paymt_calc = int(group.group_target)/group.group_members
        weekly_target = paymt_calc/4

        member = Member(weekly_target=weekly_target, monthly_target=paymt_calc, group_id=group.id, user_id=user.id)

        db.session.add(member)
        db.session.commit()

        user.group_in += 1
        db.session.commit()
        return redirect(url_for('view.group'))

@oplogic.route('/join_group', methods=['GET','POST'])
@login_required
def join_group():


    user_id = request.args.get('current_user_id')
    group_id = request.args.get('group_id')

    members  = connection.execute(
    text(f"select * from public.member where public.member.group_id = {group_id}" )
    )

    for member in members:

        user = User.query.filter_by(id=user_id).first()

        if user.id == member.user_id:
            return 'already a member to this group'

        else:
            user.group_in += 1
            db.session.commit()

            group = Group.query.filter_by(id=group_id).first()
            group.group_members += 1
            db.session.commit()

            paymt_calc = int(group.group_target)/group.group_members
            weekly_target = paymt_calc/4
            member = Member(weekly_target=weekly_target, monthly_target=paymt_calc, group_id=group.id, user_id=user.id)

            db.session.add(member)
            db.session.commit()

            return f'{user.email} successfully added to group {group.group_name}'

#Remove a member route
@oplogic.route('/remove_user')
@login_required
def remove_user():


    member_id = request.args.get('member_id')


    member = Member.query.filter_by(id=member_id).first()

    group  = Group.query.filter_by(id=member.group_id).first()

    db.session.delete(member)
    db.session.commit()

    group.group_members -= 1
    db.session.commit()

    return f'member {member.id} removed {group.group_name} member removed'


@oplogic.route('/change_admin', methods=['POST'])
@login_required
def change_admin():

    form = ChangeAdminForm()



    try:
        if form.validate_on_submit():
            group_id = int(request.args.get('group_id'))
            member_id = form.member_id.data
            password = form.password.data

            group = Group.query.filter_by(id=group_id).first()

            member = Member.query.filter_by(id=member_id).first()

            user = User.query.filter_by(id=group.group_admin).first()

            if member.group_id == group.id and password == user.password:

                group.group_admin = member.user_id
                group.user_id = member.user_id
                db.session.commit()

                return  'Groud admin successfully changed'
    except AttributeError:
        return 'group or user does not exist or check you logs'

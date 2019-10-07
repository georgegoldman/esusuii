from flask import Blueprint, flash, redirect, url_for, request, render_template, Markup
from flask_login import login_required, current_user
from .web_forms import AdminForm, GroupForm, AdduserForm, ChangeAdminForm
from .models import User, Group, Member
from . import db

oplogic = Blueprint('oplogic', __name__)

'''admin creation and group route'''

@oplogic.route('/create_admin', methods=['POST'])
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


        return redirect(url_for('view.group'))

@oplogic.route('/add_members', methods=['POST'])
@login_required
def add_member():

    form = AdduserForm()

    group_id = request.args.get('group_id')

    if form.validate_on_submit():

        email = form.email.data

        group = Group.query.filter_by(id=group_id).first()

        paymt_calc = group.group_target/(group.group_members+1)

        weekly_target = paymt_calc/4

        member = Member.query.filter_by(group_id=group_id).first()

        user = User.query.filter_by(email=email).first()

        for member_g in group.members:

            if not user:
                flash(Markup('this account don\t exist in the platform !<br><a href="/signup">click to create an account for the potential user</a>'))
                return redirect(url_for('view.home'))
            elif user.id  == member.user_id:
                flash('already a member')
                return redirect(url_for('view.add_member'))
            else:
                member = Member(weekly_target=weekly_target, monthly_target=paymt_calc, group_id=group.id, user_id=user.id)

                db.session.add(member)
                db.session.commit()

                group.group_members += 1
                db.session.commit()

                return 'successfully added to the group'
        return f'no vlidation but the group name is {group_name}'


'''Remove a member route'''
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

    return f'{group.group_name} member removed'


@oplogic.route('/change_admin')
@login_required
def change_admin():

    form = ChangeAdminForm()

    if form.validate_on_submit():
        member_id = form.member_id.data
        password = form.password.data

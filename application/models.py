from . import db
from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy.dialects.postgresql import ARRAY

class User(db.Model, UserMixin, AnonymousUserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    email = db.Column(db.Text)
    password = db.Column(db.String(80))
    group_in = db.Column(db.Integer, default = 0)
    is_admin = db.Column(db.Boolean, default=False)
    group = db.relationship('Group', backref='user', lazy='dynamic')
    member = db.relationship('Member', backref='user', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"['{self.username}']"

class Member(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    weekly_target = db.Column(db.Integer)
    monthly_target = db.Column(db.Integer)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __init__(self, username, weekly_target, monthly_target, group_id, user_id):
        self.username = username
        self.weekly_target = weekly_target
        self.monthly_target = monthly_target
        self.group_id = group_id
        self.user_id = user_id

        def __repr__(self):
            return f"['{self.id}']"

class Group(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(80))
    group_admin = db.Column(db.Integer)
    group_members = db.Column(db.Integer)
    member_limit = db.Column(db.Integer)
    group_target = db.Column(db.Integer)
    current_contribution = db.Column(db.Integer)
    members = db.relationship('Member', backref='group', lazy=True)
    paylist = db.relationship('Paylist', backref='group', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, group_name, group_admin, group_members, member_limit, group_target, current_contribution, user_id):
        self.group_name = group_name
        self.group_admin = group_admin
        self.group_members = group_members
        self.member_limit = member_limit
        self.group_target = group_target
        self.current_contribution = current_contribution
        self.user_id = user_id

    def __repr__(self):
        return f"['{self.group_name}']"

class Paylist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payee_list = db.Column(ARRAY(db.Integer), default=None)
    start_tenure = db.Column(db.Boolean, default=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __init_(self, group_id):
        self.group_id = group_id

    def __repr__(self):
        return f"[{self.payee_list}]"

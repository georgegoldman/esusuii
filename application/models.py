from . import db
from flask_login import UserMixin, AnonymousUserMixin

class User(db.Model, UserMixin, AnonymousUserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text)
    password = db.Column(db.String(80))
    is_admin = db.Column(db.Boolean)
    group = db.relationship('Group', backref='user', lazy='dynamic')
    member = db.relationship('Member', backref='user', lazy='dynamic')

    def __init__(self, email, password, is_admin=False):
        self.email = email
        self.password = password
        self.is_admin = is_admin



    def __repr__(self):
        return f'< User {self.id}>'



class Group(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(80))
    group_admin = db.Column(db.String(80))
    group_members = db.Column(db.Integer)
    group_target = db.Column(db.Integer)
    current_contribution = db.Column(db.Integer)
    member = db.relationship('Member', backref='members', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, group_name, group_admin, group_members, group_target, current_contribution, user_id):
        self.group_name = group_name
        self.group_admin = group_admin
        self.group_members = group_members
        self.group_target = group_target
        self.current_contribution = current_contribution
        self.user_id = user_id

    def __repr__(self):
        return f'<Group> {self.id}'

class Member(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    member_name = db.Column(db.Text)
    group_name = db.Column(db.Text)
    payment_scheme = db.Column(db.Integer)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __init__(self,member_name, group_name, payment_scheme, user_id, group_id):
        self.member_name = member_name
        self.group_name = group_name
        self.payment_scheme = payment_scheme
        self.user_id = user_id
        self.group_id = group_id

    def __repr__(self):
        return f'<Members {self.id}>'

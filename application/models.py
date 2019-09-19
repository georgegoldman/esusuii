from application import db
from flask_login import UserMixin

class User(db.Model, UserMixin):

    __tablename__ = 'users'
    id  = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship('Group', backref=db.backref('products', lazy='dynamic'))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Group(db.Model):

    __tablename__  = 'group'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255))
    group_admin = db.Column(db.String(255))
    number_of_member = db.Column(db.Integer)

    def __init__(self, group_name, number_of_member, group_admin):
        self.group_name = group_name
        self.group_admin = group_admin
        self.number_of_member = number_of_member

    def __repr__(self):
        return f'<user {self.username}>'

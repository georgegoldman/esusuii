from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):

    __tablename__='USERS'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

    def __init__(self, email, password, admin=None):
        self.email = email
        self.password = password
        self.admin = admin

    '''def is_admin(self):
        return self.admin'''


    def __repr__(self):
        return "< User {}>".format(self.id)



class Group(db.Model):

    __tablename__='GROUPS'

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(80))
    group_no_of_members = db.Column(db.Integer())
    group_target = db.Column(db.Integer)
    group_aggr_amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('USERS.id'))

    def __init__(self, group_name, group_members, group_target, group_aggr_amount):
        self.group_name = group_name
        self.group_members = group_members
        self.group_target = group_target
        self.group_aggr_amount = group_aggr_amount

    def __repr__(self):
        return "<Group> {}".format(self.id)

class Members(db.Model):
    __tablename__='MEMBERS'

    id = db.Column(db.Integer, primary_key=True)
    member_name = db.Column(db.Text)
    group_name = db.Column(db.Text)
    payment_scheme = db.Column(db.Integer)
    group_id = db.Column(db.Integer, db.ForeignKey('GROUPS.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('USERS.id'))


    def __init__(self,member_name, group_name, payment_scheme):
        self.member_name = member_name
        self.group_name = group_name
        self.payment_scheme = payment_scheme

    def __repr__(self):
        return "<Members {}>".format(self.id)

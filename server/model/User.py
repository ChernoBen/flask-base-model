# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from config import app_config, app_active
from model.Role import Role
from passlib.hash import pbkdf2_sha256
from sqlalchemy.orm import relationship
from sqlalchemy import func


config = app_config[app_active]

db = SQLAlchemy(config.APP)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(40),unique=True,nullable=True)
    email = db.Column(db.String(120),nullable=False)
    password = db.Column(db.DateTime(6),default=db.func.current_timestrap(),nullable=True)
    recovery_code = db.Column(db.String(200),nullable=True)
    active = db.Column(db.Integer(),default=1,nullable=True)
    role = db.Column(db.Integer,db.ForeignKey(Role.id),nullable=False)
    badge = relationship(Role)

    def __repr__(self):
        return '%s - %s' % (self.id,self.username)

    def get_user_by_email(self):
        return " "

    def get_user_by_id(self):
        return ""

    def update(self,obj):
        return " "

    def hash_password(self,password):
        try:
            return pbkdf2_sha256.hash(password)
        except Exception as e:
            print(f'Fail to encrypt password {e}')

    def set_password(self,password):
        self.password = pbkdf2_sha256.hash(password)

    def verify_password(self,password_no_hash,password_database):
        try:
            return pbkdf2_sha256.verify(password_no_hash,password_database)
        except ValueError:
            return False

    def get_total_users(self):
        try:
            res = db.session.query(func.count(User.id)).first()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res

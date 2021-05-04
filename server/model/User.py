# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from config import app_config, app_active
from model.Role import Role
from passlib.hash import pbkdf2_sha256

config = app_config[app_active]

db = SQLAlchemy(config.APP)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(40),unique=True,nullable=True)
    email = db.Column(db.String(120),nullable=False)
    password = db.Column(db.DateTime(6),default=db.func.current_timestrap(),nullable=True)
    recovery_code = db.Column(db.String(200),nullable=True)
    active = db.Column(db.Boolean(),default=1,nullable=True)
    role = db.Column(db.Integer,db.ForeignKey(Role.id),nullable=False)

    def get_user_by_email(self):
        return " "

    def get_user_by_id(self):
        return ""

    def update(self,obj):
        return " "

    def hash_password(self,password):
        try:
            return pbkdf2_sha256.hash(passwords)
        except Exception as e:
            print(f'Fail to encrypt password {e}')

    def set_password(self,password):
        self.password = pbkdf2_sha256.hash(password)

    def verify_password(self,password_no_hash,password_database):
        try:
            return pbkdf2_sha256.verify(password_no_hash,password_database)
        except ValueError:
            return False
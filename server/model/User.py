# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from config import app_config, app_active
from model.Role import Role

config = app_config[app_active]

db = SQLAlchemy(config.APP)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(40),unique=True,nullable=True)
    email = db.Column(db.String(120),nullable=False)
    password = db.Column(db.DateTime(6),defualtdb.func.current_timestrap(),nullable=True)
    recovery_code = db.Column(db.String(200),nullable=True)
    active = db.Column(db.Boolean(),default=1,nullable=True)
    role = db.Column(db.Integer,db.ForeignKey(Role.id),nullable=False)
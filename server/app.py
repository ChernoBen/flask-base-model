# -*- coding: utf-8 -*-
from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy

#codging import
from config import app_config, app_active
config = app_config[app_active]

def create_app(config_name):
    app = Flask(__name__,template_folder='templates')

    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = False
    db = SQLAlchemy(config.APP)
    db.init_app(app)

    @app.route('/')
    def index():
        return 'Hello World!'

    @app.route('/login/')
    def login():
        return 'Login return'

    @app.route('/recovery-password')
    def recovery_password():
        return 'Here is the recover screen'

    @app.route('/profile/<int:id>/action/<action>')
    def profile(id,action):
        if action == 'action1':
            return f'action choose:{action}'
        elif action == 'action2':
            return f'action choose:{action}'
        else:
            return f'Here is the ID:{id} and the action:{action} '

    @app.route('/profile/<int:id>',methods=['POST'])
    def create_profile():
        username = request.form['username']
        password = request.form['password']
        return f'This route has a put method and will edit the user name to {username} and pass to {password}'

    return app
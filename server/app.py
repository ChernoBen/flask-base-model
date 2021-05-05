# -*- coding: utf-8 -*-
from flask import Flask,request,redirect,render_template
from flask_sqlalchemy import SQLAlchemy
from controller.User import UserController
from admin.Admin import start_views
from controller.Product import ProductController

#codging import
from config import app_config, app_active
config = app_config[app_active]

def create_app(config_name):
    app = Flask(__name__,template_folder='templates')

    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'paper'
    db = SQLAlchemy(config.APP)
    db.init_app(app)
    start_views(app,db)
    db.init_app(app)

    @app.route('/')
    def index():
        return 'Hello World!'

    @app.route('/login/',methods=['POST'])
    def login():
        user = UserController()

        email = request.form['email']
        password = request.form['password']
        result = user.login(email,password)
        if result:
            return redirect('/admin')
        else:
            return render_template('login.html',data={"status":401,"message":"Invalid user data",type:None})


    @app.route('/recovery-password')
    def recovery_password():
        return 'Here is the recover screen'

    @app.route('/recovery-password/',methods=['POST'])
    def send_recovery_password():
        user = UserController()
        result = user.recovery(request.form['email'])
        if result:
            return render_template('recovery.html',data={
                "status":200,
                "message":"recovery email has been sent",
            })
        else:
            return render_template('recovery.html',data={
                "status":401,
                "message":"Fail to send the recovery email"
            })

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

    @app.route('/product',methods=['POST'])
    def save_products():
        product = ProductController()
        result = product.save_product(request.form)
        if result:
            message = "Insert"
        else:
            message = "Fail"
        return message


    return app
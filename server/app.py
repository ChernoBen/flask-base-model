# -*- coding: utf-8 -*-
from flask import Flask,request,redirect,render_template,Response,json,abort
from flask_sqlalchemy import SQLAlchemy
from controller.User import UserController
from admin.Admin import start_views
from controller.Product import ProductController
from flask_bootstrap import Bootstrap
from functools import wraps

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
    Bootstrap(app)
    start_views(app,db)
    db.init_app(app)
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin','*')
        response.headers.add('Access-Control-Allow-Headers','Content-Type')
        response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
        return response

    def auth_token_required(f):
        @wraps(f)
        def verify_token(*args,**kwargs):
            user = UserController()
            try:
                result = user.verify_auth_token(request.headers['access_token'])
                if result['status'] == 200:
                    return f(*args,**kwargs)
                else:
                    abort(result['status'],result['message'])
            except KeyError as e:
                abort(401,'Access Token is required')
        return verify_token

    @app.route('/')
    def index():
        return render_template('login.html')

    @app.route('/login/',methods=['POST'])
    def login():
        user = UserController()

        email = request.form['email']
        password = request.form['password']
        result = user.login(email,password)
        if result:
            return redirect('/admin')
        else:
            return render_template('login.html',message="This message came from route")


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

    @app.route('/product',methods=['PUT'])
    def update_products():
        product = ProductController()
        result = product.update_product(request.form)
        if result:
            message = "Updated"
        else:
            message = "Fail"
        return message

    #API endpoints :

    @app.route('/products/',methods=['GET'])
    @app.route('/products/<limit>',methods=['GET'])
    @auth_token_required
    def get_products(limit=None):
        header = {
            'access_token':request.headers['access_token'],
            "token_type":"JWT"
        }
        product = ProductController()
        response = product.get_products(limit=limit)
        return Response(json.dumps(response,ensure_ascii=False),mimetype='application/json'),response['status'],header

    @app.route('/product/<product_id>',methods=['GET'])
    @auth_token_required
    def get_product(product_id):
        header = {
            "access_token":request.headers['access_token'],
            "token_type":"JWT"
        }
        product = ProductController()
        response = product.get_product_by_id(product_id = product_id)
        return Response(json.dumps(response,ensure_ascii=False),mimetype='application/json'),response['status'],header

    @app.route('/user/<user_id>',methods=['GET'])
    @auth_token_required
    def get_user_profile(user_id):
        header = {
            "access_token": request.headers['access_token'],
            "token_type": "JWT"
        }
        user = UserController()
        response = user.get_user_by_id(user_id=user_id)
        return Response(json.dumps(response,ensure_ascii=False),mimetype='application/json'),response['status'],header


    return app
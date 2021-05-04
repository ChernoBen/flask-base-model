from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from model.Role import Role
from model.User import User
from model.Category import Category
from model.Product import Product


def start_views(app,db):
    admin = Admin(app,name= "WareHouse",template_mode="bootstrap3")
    admin.add_view(ModelView(Role,db.session,"Functions",category='Users'))
    admin.add_view(ModelView(User,db.session,"Users",category="Users"))
    admin.add_view(ModelView(Category,db.session,"Categories",category="Products"))
    admin.add_view(ModelView(Product,db.session,"Products"))
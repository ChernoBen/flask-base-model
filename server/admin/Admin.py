from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from model.Role import Role
from model.User import User
from model.Category import Category
from model.Product import Product
from admin.Views import UserView,HomeView
from flask_admin.menu import MenuLink


def start_views(app,db):
    admin = Admin(app,name= "WareHouse",base_template='admin/base.html',template_mode="bootstrap3",index_view=HomeView())
    admin.add_view(ModelView(Role,db.session,"Functions",category='Users'))
    admin.add_view(UserView(User,db.session,"Users",category="Users"))
    admin.add_view(ModelView(Category,db.session,"Categories",category="Products"))
    admin.add_view(ModelView(Product,db.session,"Products"))
    admin.add_link((MenuLink(name='Logout',url='/Logout')))


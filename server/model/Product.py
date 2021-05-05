# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from config import app_active,app_config
from model.User import User
from model.Category import Category
from sqlalchemy.orm import relationship
from sqlalchemy import func,distinct

config = app_config[app_active]
db = SQLAlchemy(config.APP)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),unique=True,nullable=False)
    description = db.Column(db.Text(),nullable=False)
    qtd = db.Column(db.Integer,nullable=True,default=0)
    image = db.Column(db.Text(),nullable=True)
    price = db.Column(db.Numeric(10,2),nullable=False)
    date_created = db.Column(db.DateTime(6),default=db.func.current_timestamp(),nullable=False)
    last_update = db.Column(db.DateTime(6),onupdate=db.func.current_timestamp(),nullable=False)
    category = db.Column(db.Integer,db.ForeignKey(Category.id),nullable=False)
    #user = relationship(User)
    type = relationship(Category)

    def get_all(self,limit):
        try:
            if limit is None:
                res = db.session.query(Product).all()
            else:
                res = db.session.query(Product).order_by(Product.data_created).limit(limit).all()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

    def update(self,obj):
        try:
            res = db.session.query(Product).filter(Product.id == self.id).update(obj)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

    def delete(self,obj):
        try:
            db.session.query(Product).filter(Product.id == self.id).delete()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(e)
            return False

    def get_total_products(self):
        try:
            res = db.session.query(func.count(Product.id)).first()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res

    def get_last_products(self):
        try:
            res = db.session.query(Product).order_by(Product.date_created).limit(5).all()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res

    def get_product_by_id(self):
        try:
            res = db.session(Product).filter(Product.id == self.id).first()
        except Exception as e:
            res = None
            print(e)
        finally:
            db.session.close()
            return res

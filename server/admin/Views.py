# -*- coding: utf-8 -*-

from flask_admin.contrib.sqla import ModelView
from config import app_config, app_active
from flask_admin import AdminIndexView,expose
config = app_config[app_active]

class HomeView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('home_admin.html',data={
            'username':'Benja'
        })

class UserView(ModelView):
    column_labels = {
        'badge':'Role',
        'username':'User name',
        'email':'E-mail',
        'date_created':'Created at',
        'last_update':'Updated at',
        'active':'Active',
        'password':'password'
    }
    column_descriptions = {
        'badge':'some description here',
        'username':'some description here',
        'date_created':'some description here',
        'last_update':'some description here',
        'active':'some description here',
        'password':'some description here'
    }
    column_exclude_list = ['password','recovery_code']
    form_excluded_columns = ['last_update','recovery_code']
    form_widget_args = {
        'password':{
            'type':'password'
        }
    }
    can_set_page_size = True
    can_view_details = True
    column_searchable_list = ['username','email']
    column_filters = ['username','email','badge']
    column_editable_list = ['username','email','badge','active']
    create_model = True
    edit_modal = True
    can_export = True
    column_sortable_list = ['username']
    column_default_sort = ('username',True)
    column_details_exclude_list = ['password','recovery_code']
    column_export_exclude_list = ['password','recovery_code']
    export_types = ['json','yaml','csv','xls','df']

    def on_model_change(self, form, model, is_created):
        if 'password' in form:
            if form.password.data is not None:
                User.set_password(form.password.data)
            else:
                del form.password
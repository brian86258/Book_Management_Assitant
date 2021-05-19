# libproject/users/views.py
from flask import Blueprint, render_template, redirect, url_for
from lib_project import db # from lib_project/__init__.py import db
from lib_project.models import Books
from lib_project.admin.forms import Add_Book_Form

users_blueprints = Blueprint('admin', __name__,template_folder='templates/admin')

@users_blueprints.route('/add_books', methods=['GET','POST'])

def add_books():

    form = Add_Book_Form()
    if form.validate_on_submit():

        B_name = form.B_name.data
        # new_user =  Users(username)
        new_book = Owned_Books(B_name,) 

        # db.session.add(new_book)
        # db.commit()

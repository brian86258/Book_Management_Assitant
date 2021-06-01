# libproject/users/views.py
from flask import Blueprint, render_template, redirect, url_for,flash, request,session
from flask_login import login_user,login_required,logout_user
from lib_project import db # from lib_project/__init__.py import db
from lib_project.models import Users, Owned_Books, Books
from lib_project.users.forms import Creaet_Users_Form, LoginForm
from flask_bootstrap import Bootstrap


users_blueprints = Blueprint('users', __name__,template_folder='templates/users')
# route/users/add_books
@users_blueprints.route('/Welcome', methods=['GET','POST'])
@login_required
def user_page():
    U_id = session['user_U_id']
    user = Users.query.filter_by(U_id=U_id).first()
    owned_books_id = user.get_books()
    owned_books = Books.query.filter(
        Books.B_id.in_(owned_books_id)
    )
    owned_books = [vars(b) for b in owned_books]

    return render_template('user_page.html', owned_books = owned_books)
    # return render_template('scann.html', owned_books = owned_books)




@users_blueprints.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('index'))


@users_blueprints.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab user from "user" by username
        user = Users.query.filter_by(username=form.username.data).first()

        if user.check_password(form.password.data) and user is not None:
            # print(user)
            # print(user.username)
            login_user(user)
            session['user_U_id']= user.U_id

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('users.user_page')

            # print(next)
            # print(login_user(user))
            return redirect(next)
        else:
            print("Fail login")

    return render_template('login.html', form=form)


@users_blueprints.route('/add_users', methods=['GET','POST'])
def add_users():
    form = Creaet_Users_Form()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        phone = form.phone.data

        new_user = Users(username,password,email,phone)
        db.session.add(new_user)

        # KEY, Still need to handling error message
        try:
            db.session.commit()
            return redirect(url_for('index'))
            # return render_template('home.html')
        except Exception as e:
            # flash("Something wrong when creating NEW USERS")
            # flash("Fowllowing is error message", e)
            print("Fowllowing is error message", e)


    return render_template('create_users.html', form = form)

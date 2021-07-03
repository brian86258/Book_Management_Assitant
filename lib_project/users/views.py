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
    
    search_item = ''
    if request.method =='POST':
        # Receive form to add books
        if request.values['send']=='search_books':
            search_item = request.values['book']
            print(search_item)
        if request.values['send']=='delete':
            del_B_id = request.values['del_B_id']
            Owned_Books.query.filter(
                (Owned_Books.U_id == U_id) & (Owned_Books.B_id == del_B_id)
            ).delete()
            db.session.commit()
            print('Delete Book {}'.format(del_B_id))
        


    user = Users.query.filter_by(U_id=U_id).first()
    owned_books_id = user.get_books()
    owned_books = Books.query.filter(
        Books.B_id.in_(owned_books_id)
    )
    owned_books = [vars(b) for b in owned_books]

    if search_item:
        owned_books = [book for book in owned_books if search_item.lower() in book['title'].lower() or search_item.lower() in book['authors'].lower()]
    # print(owned_books)
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

        if user and user.check_password(form.password.data):
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
            return render_template('login.html', form=form,login_message = "Failed Login. Please Try Again!")

    return render_template('login.html', form=form, login_message="")


@users_blueprints.route('/add_users', methods=['GET','POST'])
def add_users():
    form = Creaet_Users_Form()
    usr_err_msg = ''
    email_err_msg = ''
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        phone = form.phone.data
        user = Users.query.filter(
                (Users.email == email) | (Users.username == username) 
            ).first()
        if not user:
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
                err_msg = e
        else: # If such user exist
            if email == user.email:
                email_err_msg = "This email address has already been used, please use another one"
            if username == user.username:
                usr_err_msg = "This username already has been used, please use another one"

            return render_template('create_users.html', form = form, usr_err_msg = usr_err_msg, email_err_msg = email_err_msg)



    return render_template('create_users.html', form = form, usr_err_msg = usr_err_msg, email_err_msg = email_err_msg)

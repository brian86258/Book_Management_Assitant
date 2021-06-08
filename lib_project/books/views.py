from operator import or_
from flask import Blueprint, render_template, redirect, url_for,flash, session, request
from lib_project import db # from lib_project/__init__.py import db
from lib_project.models import Books, Owned_Books,Users
from lib_project.books.forms import Search_Book_Form
from lib_project.search_books import search_book
from sqlalchemy import func
import datetime

books_blueprints = Blueprint('books', __name__,template_folder='templates/books')

@books_blueprints.route('/search_books',methods=['GET','POST'])
def search_books():
    form = Search_Book_Form()
    if form.validate_on_submit():
        search = form.search.data
        # print(search)
        # print(type(search))

        books_list = search_book(search)
        session['books_list'] = books_list
        # print(books_list)
        return redirect(url_for('books.search_result'))
        # return render_template('results.html', books_list = books_list)
    return render_template('search_books.html', form = form)

@books_blueprints.route('/search_result', methods=['GET',"POST"])
def search_result():
    books_list = session['books_list']

    if request.method =='POST':
        # Receive form to add books
        if request.values['send']=='Add to Shelves':
            title = request.values['title']
            categories = request.values['categories']
            published_date = request.values['published_date']

            # published_date = datetime.datetime.strptime(published_date,'%Y-%m-%d').date()
            authors = request.values['authors']
            img_url = request.values['img_url']
            ISBN_13 = request.values['ISBN_13']
            ISBN_10 = request.values['ISBN_10']
            purchase_url = request.values['purchase_url']

            # Check if this book is already in shelves
            Book = Books.query.filter(
                (Books.ISBN_10 == ISBN_10) | (Books.ISBN_13 == ISBN_13) | (Books.title == title)
            ).first()
            new_book = Books(title,categories,published_date,authors,img_url,ISBN_13,ISBN_10,purchase_url)
            db.session.add(new_book)
            db.session.commit()

            # If this Book is not in the shelves, add to the shelves
            if not Book:
                new_book = Books(title,categories,published_date,authors,img_url,ISBN_13,ISBN_10,purchase_url)
                print('NOT IN SHELF')
                max_idx = db.session.query(func.max(Books.B_id)).scalar()
                B_id = max_idx +1
                print(B_id)
                db.session.add(new_book)
                # KEY, Still need to handling error message
                try:
                    print('Successfully add to Public shelf!')
                    db.session.commit()
                    # return render_template('home.html')
                except Exception as e:
                    # flash("Something wrong when creating NEW USERS")
                    # flash("Fowllowing is error message", e)
                    db.session.rollback()
                    print("Fowllowing is error message", e)
            else:
                print(" ALREADY IN SHELF")
                B_id = Book.B_id
                # print(Book.B_id)
            # return redirect(url_for('index'))
            

        # After in the shelves build up connection with users
        print(session['user_U_id'])
        if session['user_U_id']:
            U_id = session['user_U_id']
            print(U_id)
            print(B_id)
            user = Users.query.filter_by(U_id=U_id).first()
            owned_books_id = user.get_books()
            if B_id in owned_books_id:
                print("Already in personal Shelf")
                return redirect(url_for('users.user_page'))

            new_owned_book = Owned_Books(U_id=U_id, B_id=B_id)
            try:
                db.session.add(new_owned_book)
                db.session.commit()
                print('Successfully add to personal shelf!')
                return redirect(url_for('users.user_page'))

            except Exception as e:
                db.session.rollback()
                print("Following is error message{}".format(e))

    return render_template('results.html', books_list = books_list)



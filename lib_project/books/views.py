from flask import Blueprint, render_template, redirect, url_for,flash, session, request
from lib_project import db # from lib_project/__init__.py import db
from lib_project.models import Books
from lib_project.books.forms import Search_Book_Form
from lib_project.search_books import search_book
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
        if request.values['send']=='Add to Shelves':
            title = request.values['title']
            categories = request.values['categories']
            published_date = request.values['published_date']

            # published_date = datetime.datetime.strptime(published_date,'%Y-%m-%d').date()
            authors = request.values['authors']
            img_link = request.values['img_link']
            ISBN_13 = request.values['ISBN_13']
            ISBN_10 = request.values['ISBN_10']
            purchase_link = request.values['purchase_link']
            new_book = Books(title,categories,published_date,authors,img_link,ISBN_13,ISBN_10,purchase_link)
            
            db.session.add(new_book)
                    # KEY, Still need to handling error message
            try:
                flash("Successful")
                db.session.commit()
                return redirect(url_for('index'))
                # return render_template('home.html')
            except Exception as e:
                # flash("Something wrong when creating NEW USERS")
                # flash("Fowllowing is error message", e)
                print("Fowllowing is error message", e)


            # print(request.values['title'])
    return render_template('results.html', books_list = books_list)



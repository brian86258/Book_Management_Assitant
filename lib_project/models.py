# KEY this files is used to seting up 
# SQLite stores db
from lib_project import db, login_manager
from datetime import datetime,date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# Step1. 在一對多的一中設定 db.relationship(…) 關係
# Step2. 在一對多的多中設定 db.ForeignKey(…) 關係

# The user_loader decorator allows flask-login to load the current user
# and grab their id.
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    U_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64),unique = True, nullable=False)
    password_hash = db.Column(db.String(128), nullable = False)
    email = db.Column(db.String(64), unique = True, nullable = False)
    phone = db.Column(db.String)
    owned_books = db.relationship("Owned_Books",backref='users')
    created_time = db.Column(db.DateTime, default=datetime.now, nullable=False)

    # created_time = db.DateTime(onupdate=datetime.now, default=datetime.now, nullable=False)

    def __init__(self, username, password, email = "None", phone="None", created_time=datetime.now()):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.email = email
        self.phone = phone
        self.created_time = created_time
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.U_id

    def __repr__(self):
        return_obj = {
            'U_id' : self.U_id,
            'username' : self.username,
            'email' : self.email,
            'phone' : self.phone,
            'created_time': self.created_time,
            'owned_books': None
        }
        if self.owned_books:
            return_obj['owned_books'] = self.owned_books

        return return_obj

    def get_books(self):
        books = []
        for book in self.owned_books:
            books.append(book.B_id)
        return books

            
    

class Books(db.Model):
    __tablename__ = 'books'
    B_id = db.Column(db.Integer, primary_key = True)
    ISBN_10 = db.Column(db.Integer)
    ISBN_13 = db.Column(db.Integer)
    title = db.Column(db.Text)
    img_url = db.Column(db.Text)
    authors = db.Column(db.Text)
    # descr = db.Column(db.Text)
    purchase_url = db.Column(db.Text)
    published_date = db.Column(db.Text)
    created_time = db.Column(db.DateTime, default=datetime.now, nullable=False)

    users_owned = db.relationship("Owned_Books",backref='books')
    
    def __init__(self, title,categories,published_date,authors,img_url,ISBN_13,ISBN_10,purchase_url, created_time=datetime.now()):
        self.title = title
        self.categories = categories
        self.published_date = published_date
        self.authors = authors
        self.img_url = img_url
        self.ISBN_13 = ISBN_13
        self.ISBN_10 = ISBN_10
        self.purchase_url = purchase_url
        self.created_time = created_time

    def __repr__(self):
        return_obj = {
            "B_id": self.B_id,
            "categories" : self.categories,
            "title": self.title,
            "published_date" : self.published_date,
            'authors': self.authors,
            "img_link": self.img_link,
            'ISBN_13': self.ISBN_13,
            'ISBN_10': self.ISBN_10,
            "purchase_link": self.purchase_link,
            "created_time": self.created_time 
        }
        if self.users_owned:
            return_obj['users_owned'] = self.users_owned
    
    def get_owners(self):
        owners = []
        for owner in self.users_owned:
            owners.append(owner.U_id)
        return owners





class Owned_Books(db.Model):
    __tablename__ = 'owned_books'
    B_id = db.Column(db.Integer, db.ForeignKey('books.B_id'), primary_key= True)
    U_id = db.Column(db.Integer, db.ForeignKey('users.U_id'), primary_key= True,)
    created_time = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __init__(self, U_id,B_id, created_time=datetime.now()):
        self.U_id = U_id
        self.B_id = B_id
        self.created_time = created_time
    








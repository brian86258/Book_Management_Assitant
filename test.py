from lib_project.models import Users,Books,Owned_Books
from lib_project import db # from lib_project/__init__.py import db

# *** ADD DATA****
user = Users.query.filter_by(username = 'manager').all()
books = Books.query.filter(
    Books.ISBN_13.like("%986%")
)
for u in user:
    if u:
        print('-',u.U_id)
        for b in books:
            print('*',b.B_id)
            new_owned_book = Owned_Books(u.U_id, b.B_id)
            
            db.session.add(new_owned_book)
            db.session.commit()


# user = Users.query.filter_by(username = 'manager').first()
# # print(vars(user))
# own_books_id = user.get_books()
# print(own_books_id)

# # query_in
# owned_books = Books.query.filter(
#     Books.B_id.in_(own_books_id)
# )

# # print(vars(owned_books))
# owned_books = [vars(b) for b in owned_books]
# for book in owned_books:
#     # book = Books.query.filter_by(B_id = book).first()
#     print(type(book))
#     print(book)
    # print(type(vars(book)))





# for u in user:
#     if u:
#         print(vars(user[0]))

# books = Books.query.filter(
#     Books.ISBN_13.like("%986%")
# )

# for b in books:
#     if b:
#         print(b.B_id)




# *** ADD DATA****
# for u in user:
#     if u:
#         print('-',u.U_id)
#         for b in books:
#             print('*',b.B_id)
#             new_owned_book = Owned_Books(u.U_id, b.B_id)
            
#             db.session.add(new_owned_book)
#             db.session.commit()

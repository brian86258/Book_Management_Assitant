from lib_project import app
from lib_project import db
from flask import render_template


@app.route('/')
def index():
   db.create_all()
   return render_template('home.html')

if __name__ =='__main__':
    app.run(debug=True)
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from datetime import datetime

SQLALCHEMY_TRACK_MODIFICATIONS = True

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_pasta.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Pasta(db.Model):
    current_date = datetime.now()
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=current_date)

    def __repr__(self):
        return '<Pasta %r>' % self.id


@app.route('/')
def null_page():
    return render_template("about.html")


@app.route('/home')
def home():
    articles = Pasta.query.order_by(Pasta.date.desc()).all()
    return render_template("home.html", articles=articles)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/sign', methods=['POST', 'GET'])
def create_pasta():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        pasta = Pasta(title=title, intro=intro, text=text)

        try:
            db.session.add(pasta)
            db.session.commit()
            return redirect('/about')
        except:
            return "При создании пасты произошла ошибка"
    else:
        return render_template("base-create-post.html")


'''
@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "User page: " + name + " - " + str(id)
'''

if __name__ == "__main__":
    app.run(debug=True)
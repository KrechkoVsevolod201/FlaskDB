from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3
SQLALCHEMY_TRACK_MODIFICATIONS = True

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return 'Account %r' % self.id


@app.route('/')
def null_page():
    return render_template("about.html")


@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/sign', methods=['POST', 'GET'])
def create_account():
    if request.method == "POST":
        username = request.form['username']
        comment = request.form['comment']

        account = Account(username=username, comment=comment)

        try:
            db.session.add(account)
            db.session.commit()
            return redirect('/about')
        except:
            return "При создании пользователя произошла ошибка"
    else:
        return render_template("base-create-post.html")


'''
@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "User page: " + name + " - " + str(id)
'''

if __name__ == "__main__":
    app.run(debug=True)
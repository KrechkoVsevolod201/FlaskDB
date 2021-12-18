from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import  sqlite3
SQLALCHEMY_TRACK_MODIFICATIONS = True

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(300), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return 'Account %r' % self.id

@app.route('/')
def home():
    return render_template("about.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/home', methods=['POST', 'GET'])
def create_account():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        account = Account(username=username, password=password)

        try:
            db.session.add(account)
            db.session.commit()
            return redirect('/about')
        except:
            return "При создании пользователя произошла ошибка"
    else:
        return render_template("base-sign.html")


'''
@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "User page: " + name + " - " + str(id)
'''

if __name__ == "__main__":
    app.run(debug=True)
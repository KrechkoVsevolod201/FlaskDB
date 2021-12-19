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


@app.route('/posts/<int:id>')
def pasta_detail(id):
    article = Pasta.query.get(id)
    return render_template("post-detail.html", article=article)


@app.route('/posts/<int:id>/del')
def pasta_delete(id):
    article = Pasta.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/home')

    except:
        return "При удалении пасты произошла ошибка"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def pasta_update(id):
    pasta = Pasta.query.get(id)
    if request.method == "POST":
        pasta.title = request.form['title']
        pasta.intro = request.form['intro']
        pasta.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/about')
        except:
            return "При редактировании пасты произошла ошибка"
    else:
        return render_template("post_update.html", pasta=pasta)


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
        return render_template("create-post.html")


'''
@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "User page: " + name + " - " + str(id)
'''

if __name__ == "__main__":
    app.run(debug=True)
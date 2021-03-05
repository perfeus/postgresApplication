# для выполнения миграций установить Flask-Migrate
# для доступа к PostgreSQL в SQLAlchemy установить psycopg2-binary

import os

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'mysuperkey'
# Настраиваем приложение
# app.config["DEBUG"] = True

# - URL доступа к БД берем из переменной окружения DATABASE_URL
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Создаем подключение к БД
db = SQLAlchemy(app)
# Создаем объект поддержки миграций
migrate = Migrate(app, db)

#Модель для хранения визитов нашей страницы
class Visit(db.Model):
    # Таблица
    __tablename__ = 'names'

    id = db.Column(db.Integer, primary_key=True)
    # Имя пользователя
    name = db.Column(db.String, nullable=False)

class FirstForm(FlaskForm):
    name = StringField("Name", [InputRequired()])
    submit = SubmitField("Submit")

# Наша единственная страница
@app.route('/', methods=["POST", "GET"])
def home():
    form = FirstForm()
    if request.method == "POST":
        name = form.name.data
        user = Visit(name=name)
        db.session.add(user)
        db.session.commit()
        users = db.session.query(Visit).all()

        return render_template("home.html", form=form, name=name, users=users)
    return render_template("home.html", form=form)


if __name__ == "__main__":
    app.run(debug=False)
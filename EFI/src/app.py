from flask import Flask, render_template, request, redirect, url_for, flash

from flask_sqlalchemy import SQLAlchemy

from config import config

# model
from models.ModelUser import ModelUser

# entities
from models.entities.User import Usuario


app = Flask(__name__)

db = SQLAlchemy(app)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form['username'])
        # print(request.form['password'])
        user = Usuario(request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                return redirect(url_for('home'))
            else:
                flash("Password invalido!!")
                return render_template('auth/login.html')    
        else:
            flash("Usuario no encontrado!!")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/home')
def home():
    return render_template('home.html')


    
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
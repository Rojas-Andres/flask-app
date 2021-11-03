from flask import Flask, render_template, request, redirect, url_for, flash,session,jsonify, make_response
from db.db import Session , engine,connection_db
from werkzeug.security import generate_password_hash,check_password_hash
import json
import jwt
from functools import wraps
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY']='Th1s1ss3cr3t'
app.config['SQLALCHEMY_DATABASE_URI'] = connection_db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

#token de pagina
def require_api_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        try:
            # validamos que el token aun este activo
            data = jwt.decode(session["token-key"], app.config['SECRET_KEY'])
        except:
            # Borramos toda la session
            session.clear()
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return check_token

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('Index'))
    else:
        return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        return redirect(url_for('Index'))
    else:
        return render_template('registro.html')

@app.route('/')
@require_api_token
def Index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
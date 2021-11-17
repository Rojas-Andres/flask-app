from flask import Flask, render_template, request, redirect, url_for, flash,session,jsonify, make_response
from db.db import Session , engine,connection_db
from werkzeug.security import generate_password_hash,check_password_hash
import json
import jwt
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from validate import *
from functions import *
import datetime
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
            data = jwt.decode(session["token"], app.config['SECRET_KEY'])
        except:
            # Borramos toda la session
            session.clear()
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return check_token

@app.route('/login', methods=['GET', 'POST'])
def login():
    context={
        "message":"",
        "type":""
    }
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        user = valida_user(username)
        if user : 
            if check_password_hash(user[2], password):  
                token = jwt.encode({'public_id': user[1], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])  
                session["token"] = token.decode('UTF-8')
                session["usuario"] = user[1]
                # Realizar insert 
                val = update_or_insert(username)
                if val==1:
                    return redirect(url_for('cambiarpass'))

                return redirect(url_for('Index'))
            else:
                context={
                    "message":"Usuario/contraseña inválidos",
                    "type":"danger"
                }
                return render_template('login.html',context=context)
        else:
            context={
                    "message":"usuario/contraseña inválidos",
                    "type":"danger"
            }
            return render_template('login.html',context=context) 
    else:
        return render_template('login.html',context=context)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    context={
        "message":"",
        "type":""
    }
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        cant_intentos = int(request.form["cant_intentos"])
        if cant_intentos==0:
            context={
                "message":"La cantidad de intentos debe de ser mayor a 0",
                "type":"danger"
            }
            return render_template('registro.html',context=context)
        context = valida_password(password)
        if context["type"]=="danger":
            return render_template('registro.html',context=context)
        try:
            hash_password = generate_password_hash(password,method="sha256")
            engine.execute(f""" INSERT INTO usuario(username,password,cant_intentos) values('{username}','{hash_password}',{cant_intentos})""")
            insert_contra_guardadas(username,hash_password)    
        except:
            context={
                "message":"El usuario ya existe en la base de datos intente otro",
                "type":"danger"
            }
            return render_template('registro.html',context=context)
        return render_template('registro.html',context=context)
    else:
        context ={
            "message":"Recuerde debe tener mínimo una minúscula, una mayúscula, un caracter especial, un número, minimo de 8 caracteres, máximo de 15 caracteres",
            "type":"success"
        }
        return render_template('registro.html',context=context)
@app.route('/salir', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))
@app.route('/')
@require_api_token
def Index():
    usuario = session["usuario"]
    return render_template('index.html',usuario=usuario)
@app.route('/cambiarpass', methods=['GET', 'POST'])
@require_api_token
def cambiarpass():
    context={
        "message":"",
        "type":""
    }
    if request.method == 'POST':
        password = request.form["password"]
        context = valida_password(password)
        if context["type"]=="danger":
            return render_template('cambiar_pass.html',usuario=session["usuario"],context=context)
        hash_password = generate_password_hash(password,method="sha256")
        
        valor = validate_password(session["usuario"],password)
        if valor == 1:
            context["type"] = "danger"
            context["message"] = "Esta contraseña ya la ha usado intente otra"
            return render_template('cambiar_pass.html',usuario=session["usuario"],context=context) 
        actualizar_contra(session["usuario"],hash_password)
        actualizar_intentos(session["usuario"])
        insert_contra_guardadas(session["usuario"],hash_password)
        return redirect(url_for('logout'))
    return render_template('cambiar_pass.html',usuario=session["usuario"],context=context)
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
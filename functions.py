from db.db import Session , engine,connection_db
from querys import Query
from validate import *
from werkzeug.security import generate_password_hash,check_password_hash

query = Query()
def valida(lista,cadena):
    for i in cadena:
        if i in lista:
            return 1
    return 0
def valida_user(username):
    with engine.connect() as con:
        try:
            user = con.execute(f"select * from usuario where username='{username}'").one()
        except:
            user = None 
        return user
def valida_password(password):
    context={}
    if ' ' in password:
        context["message"] = "La contraseña no debe de tener espacios"
        context["type"] = "danger"
        return context       
    if len(password)<8:
        context["message"] = "La longitud de la contraseña debe de ser mayor a 8"
        context["type"] = "danger"
        return context
    if len(password)>15:
        context["message"] = "La longitud de la contraseña debe de ser menor que 15"
        context["type"] = "danger"
        return context
    val = valida(numeros,password)
    if val==0:
        context["message"] = "La contraseña debe de tener al menos un numero"
        context["type"] = "danger"
        return context         
    val = valida(letras_min,password)
    if val==0:
        context["message"] = "La contraseña debe de tener al menos una letra minuscula"
        context["type"] = "danger"
        return context  
    val = valida(letras_max,password)
    if val==0:
        context["message"] = "La contraseña debe de tener al menos una letra mayuscula"
        context["type"] = "danger"
        return context  
    val = valida(simbolos,password)
    if val==0:
        context["message"] = "La contraseña debe de tener al menos un caracter especial"
        context["type"] = "danger"
        return context    
    context["message"] = "Usuario creado satisfactoriamente"
    context["type"] = "success"
    return context  

def update_or_insert(username):
    user = engine.execute(query.valida_user_int(username)).one()
    print(user)
    if user[0]==0:
        engine.execute(query.insertar_user_intentos(username))
        return 0
    else:
        valor = engine.execute(query.intentos(username)).one()
        print("EL VALOR ES : ",valor)
        if valor[0] == 1:
            return 1
        else:
            #Sumar 1 a los intentos 
            id = engine.execute(query.devuelve_id_usuario(username)).one()
            engine.execute(query.actualiza_intentos(id[0]))
            return 0
def actualizar_contra(username,password):
    engine.execute(query.update_password(username,password))

def actualizar_intentos(username):    
    id = engine.execute(query.devuelve_id_usuario(username)).one()
    engine.execute(query.actualizar_intentos(id[0]))
def insert_contra_guardadas(username,password):
    id = engine.execute(query.devuelve_id_usuario(username)).one()
    engine.execute(query.insertar_contra_guardadas(id[0],password))
def validate_password(username,password):
    id = engine.execute(query.devuelve_id_usuario(username)).one()
    passwords = engine.execute(query.obtener_todas_pass_user(id[0])) 
    all = passwords.fetchall()
    
    all = [i[0] for i in all ]
    for i in all:
        print(i)
        if check_password_hash(password, i):
            print("LA CONTRASEÑA EXISTE")
            
    return 1
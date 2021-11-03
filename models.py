from sqlalchemy import Column,String , Integer 
#from db import Base,engine
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from app import db

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer,autoincrement=True , primary_key=True)
    username = db.Column(db.String(70),unique=True)
    password = db.Column(db.String(200))
    cant_intentos = db.Column(db.Integer(200))
    intentos = relationship('Intentos',backref="usuario",cascade="delete,merge")
    contrasGuardadas = relationship('ContrasGuardadas',backref="usuario",cascade="delete,merge")

class ContrasGuardadas(db.Model):
    __tablename__ = 'contrasGuardadas'
    id = db.Column(db.Integer,autoincrement=True , primary_key=True)
    username_id = db.Column(db.Integer,ForeignKey("usuario.id",ondelete="CASCADE"))
    password = db.Column(db.String(200))

class Intentos(db.Model):
    __tablename__ = 'intentos'
    id = db.Column(db.Integer,autoincrement=True , primary_key=True)
    username_id = db.Column(db.Integer,ForeignKey("usuario.id",ondelete="CASCADE"))

#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-06,9:45"
import pymysql
pymysql.install_as_MySQLdb()

from flask_login import UserMixin
from . import db


class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column (db.Integer,primary_key = True)
    username = db.Column (db.String (64),unique = True)
    password = db.Column (db.String (64))
    def __repr__(self):
        return self.username



class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    title = db.Column(db.String(20),nullable = False)
    price = db.Column(db.Float,nullable = True)
    author = db.Column(db.String(20),nullable = True)
    publish = db.Column(db.String(20),nullable = False)

    def __repr__(self):
        return self.title
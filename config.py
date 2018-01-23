#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-06,9:20"
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.urandom (24)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/flaskpro?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass

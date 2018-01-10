#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-10,14:04"
from flask import session,redirect,url_for,request


class Auth(object):
    def __init__(self,app = None):
        self.app = app
        if app:
            self.init_app(app)
    def init_app(self,app):
        app.auth_manager = self
        app.before_request(self.check_login)
        app.context_processor(self.auth_context_processor)
    def check_login(self):
        if session.get("user_info") or request.path  in ["/login","/register"] :
            return None
        return redirect (url_for ("main.login"))
    def auth_context_processor(self):
        name = session.get("user_info")
        return dict(current_user = name)

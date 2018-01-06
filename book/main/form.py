#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-06,9:47"
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms import PasswordField
from wtforms import FloatField
from wtforms.validators import Required
from wtforms.validators import EqualTo



class RegisterForm(FlaskForm):
    username = StringField("用户名:",validators = [Required(message = "用户名不能为空")],render_kw = {"placeholder":"请输入用户名"})
    password = PasswordField("密码:",validators = [Required(message = "密码不能为空")],render_kw = {"placeholder":"请输入密码"})
    password2 = PasswordField("重复密码:",validators = [Required(message = "密码不能为空"),EqualTo("password",message = "两次输入的密码不一致")],render_kw = {"placeholder":"请再次输入密码"})
    submit = SubmitField("提交")

class AddBookForm(FlaskForm):
    title = StringField("书名:",validators = [Required(message = "书名不能为空")])
    price = FloatField("价格:",validators = [Required(message = "价格不能为空")])
    author = StringField("作者:",validators = [Required(message = "作者不能为空")])
    publish = StringField("出版社:",validators = [Required(message = "出版社不能为空")])
    submit = SubmitField ("提交")
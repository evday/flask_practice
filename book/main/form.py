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
from wtforms import Form

# 创建这个Form类的时候会执行一个函数def with_metaclass 这个方法就已经给RegisterForm 类里面增加了连个新的字段 _unbound_fields = None 和 _wtforms_meta = None
class RegisterForm(FlaskForm):
    # 这是第二步 实例化StringField 会执行它的new方法，自己没有就去Field 这个类里面找 发现返回了一个UnboundField 对象

    username = StringField("用户名:",validators = [Required(message = "用户名不能为空")],render_kw = {"placeholder":"请输入用户名"})
    password = PasswordField("密码:",validators = [Required(message = "密码不能为空")],render_kw = {"placeholder":"请输入密码"})
    password2 = PasswordField("重复密码:",validators = [Required(message = "密码不能为空"),EqualTo("password",message = "两次输入的密码不一致")],render_kw = {"placeholder":"请再次输入密码"})
    submit = SubmitField("提交")

     # username 是 UnboundField 的一个对象  creation_counter = 1
     # password 是 UnboundField 的一个对象  creation_counter = 2 这个creation_counter 是控制页面上input 框的显示顺序的
class AddBookForm(FlaskForm):
    title = StringField("书名:",validators = [Required(message = "书名不能为空")])
    price = FloatField("价格:",validators = [Required(message = "价格不能为空")])
    author = StringField("作者:",validators = [Required(message = "作者不能为空")])
    publish = StringField("出版社:",validators = [Required(message = "出版社不能为空")])
    submit = SubmitField ("提交")


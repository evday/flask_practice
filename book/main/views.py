#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-06,9:45"
import json
import time
from flask import flash,redirect,url_for,render_template,request,session
from .form import RegisterForm,AddBookForm
from ..models import User,Book
from .pager import Pagination
from . import main
from .. import db




@main.before_request
def process_request():
    if request.path  in ["/login","/register"] :
        return None
    else:
        user = session.get("user_info")
        if not user:
            return redirect(url_for("main.login"))

@main.route ('/login',methods = ["GET","POST"],endpoint = "login")
def hello_world ():
        if request.method == "GET":
            return render_template ("login.html")
        elif request.method == "POST":
            state = {"state":None}
            username = request.form.get ("user")
            if username == "":
                state ["state"] = "user_none"
                return  json.dumps (state)
            password = request.form.get ("pwd")
            if password == "":
                state ["state"] = "pwd_none"
                return json.dumps (state)
            user =  User.query.filter_by(username=username,password=password).first()
            if user:

                state ["state"] = "login_success"
                session ['user_info'] = user.username
            else:
                state ["state"] = "failed"
            return json.dumps (state)
@main.route("/register",methods = ["GET","POST"],endpoint = "register")
def register():

    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user = User(username = form.username.data,password = form.password.data)
            db.session.add(user)
            db.session.commit ()
            flash("注册成功")
            return redirect(url_for("main.login"))
        except:
            flash("账号已存在")
            return redirect(url_for("main.register"))
    return render_template('register.html',form=form)
@main.route("/logout",endpoint = "logout")
def logout():
    session.clear()
    flash("你已经退出了")
    return redirect(url_for("main.login"))

@main.route('/book',methods = ["GET"],endpoint = "book")
def book():

    book_list = Book.query.all ()
    pager_obj = Pagination (request.args.get ('page',1),len (book_list),request.path,request.args)
    host_list = book_list [pager_obj.start:pager_obj.end]
    html = pager_obj.page_html ()

    return render_template("book_list.html",book_list=host_list,html=html,session=session)

@main.route("/delete/<book_id>",endpoint = "delete")
def delete(book_id):
    delete_book = Book.query.filter_by(id=book_id).first()
    db.session.delete(delete_book)
    db.session.commit()
    return redirect(url_for('main.book'))
@main.route("/add",methods = ["GET","POST"],endpoint = "add_book")
def add():

    form = AddBookForm()
    if form.validate_on_submit():
        book = Book(title = form.title.data,price=form.price.data,author = form.author.data,publish = form.publish.data)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for("main.book"))
    return render_template("add.html",form=form)

@main.route("/edit/<book_id>",endpoint = "edit",methods = ["GET","POST"])
def edit(book_id):

    edit_book = Book.query.filter_by (id = book_id).first ()
    form = AddBookForm(title=edit_book.title,price=edit_book.price,author=edit_book.author,publish=edit_book.publish)
    if form.validate_on_submit():
        book = Book ()
        book.id = int(book_id)
        book.title = form.title.data
        book.price = form.price.data
        book.author = form.author.data
        book.publish = form.publish.data
        db.session.merge(book)
        db.session.commit()
        return redirect(url_for("main.book"))
    return render_template('edit.html',form=form)
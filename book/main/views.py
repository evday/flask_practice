#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-06,9:45"
import json
import time
from flask import flash,redirect,url_for,render_template,request,session
from .form import RegisterForm,AddBookForm
from ..models import User,Book
from .pager import Pagination
from .pool import SingletonDBPool
from . import main
from .. import db




# @main.before_request
# def process_request():
#     if request.path  in ["/login","/register"] :
#         return None
#     else:
#         user = session.get("user_info")
#         if not user:
#             return redirect(url_for("main.login"))

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
    # 这是 第三步 实例化RegisterFrom 实例化要执行Form 类的__init__ 方法 在执行 Form 类的__init__方法之前 会执行它父类的__call__方法
    # 这个RegisterForm 继承FlaskForm--》 Form-->NewBas这个类，而这个类是由FormMeta 创建的 所以 RegisterForm() 这一步会执行FormMeta的__call__
    # 这个时候__wtforms_meta 和 _unbound_fields 里面就有值了
    # 然后这里会执行Form 的__init__ 方法

    # 创建这个类 的__call__方法
            # RegisterForm._unbound_fields 里面,里面已经有值了 是一个列表 [(name,UnboundField对象)]
            # RegisterForm._wtforms_meta 是一个类 Meta(Meta) 这个类继承了所有的类
    # 这个类的__new__ 方法
    # 这个类的__init__ 方法
            #实例化 Meta --> meta_obj
            # 在UnboundField 对象调用bind 这个方法的时候对StringField等类进行实例化
            #self._fields = {
            #username = StringField()
            #password = PasswordField()
    # }
            # self.name =  StringField()
            # self.pwd = PasswordField()
    # 这里用了两遍才将StringField 类实例化 为什么呢
    # 这里相当于做了一次缓存，在实例化Form 的时候 先将数据查找了一遍RegisterForm._unbound_fields ，如果有值的时候就不用再找了
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

    pool = SingletonDBPool()
    conn = pool.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM book;")
    book_list = cursor.fetchall()

    cursor.close()
    conn.close()

    # book_list = Book.query.all ()
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
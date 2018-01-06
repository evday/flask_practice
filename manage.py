#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-06,10:10"

from flask_script import Manager

from book import create_app

app = create_app()
manager = Manager(app)



if __name__ == '__main__':
    app.run(debug = True)
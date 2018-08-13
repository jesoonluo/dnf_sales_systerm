#! /usr/bin/env python3.4
# -*- coding: utf-8 -*-
# author: notedit<notedit@gmail.com>
import json
import datetime

from db import db, app
from decimal import Decimal
from flask import current_app
from flask_script import Manager, prompt, prompt_pass, prompt_bool, prompt_choices
from flask_script import Server


manager = Manager(app)

@manager.command
def initdb():
    if prompt_bool("Are you sure? You will init your database"):
        db.create_all()


@manager.command
def dropdb():
    if prompt_bool("Are you sure? You will lose all your data!"):
        db.drop_all()


manager.add_command('runserver',Server())

@manager.shell
def make_shell_context():
    return dict(app=app,db=db)

if __name__ == '__main__':
    manager.run()

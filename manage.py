# -*- coding: utf-8 -*-

from dnf_sys import db, app
from flask_script import Manager, prompt_bool, Server
from dnf_sys.model import userModel

manager = Manager(app)

@manager.command
def initdb():
    if prompt_bool("Are you sure? You will init your database"):
        db.create_all()


@manager.command
def dropdb():
    if prompt_bool("Are you sure? You will lose all your data!"):
        db.drop_all()


manager.add_command('runserver',Server(host='0.0.0.0', port=8888))

@manager.shell
def make_shell_context():
    return dict(app=app,db=db)

if __name__ == "__main__":
    manager.run()

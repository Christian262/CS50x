from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bibitybop'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeD8goaAAAAAJYxZPJhp9y2gPWZxP8P_qlqLv0W'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeD8goaAAAAAF2tCKrpWqBlSq6reGY0FFZ9RODs'
app.config['TESTING'] = True

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from raceworld import routes

if __name__ == '__main__':
    manager.run()
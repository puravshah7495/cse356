from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime

db = SQLAlchemy()

class Users(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	password = db.Column(db.String(255), nullable=False)
	email = db.Column(db.String(255), unique=True, nullable=False)
	verified = db.Column(db.Boolean(), nullable=False, default=False)

	def __init__(self, username, password, email):
		self.username = username
		self.password = password
		self.email = email

class VerifyKeys(db.Model):
	__tablename__ = 'verifykeys'
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
	emailed_key = db.Column(db.String(100))

	user = db.relationship('Users', backref='verifykey')

	def __init__(self, user_id, emailed_key):
		self.user_id = user_id
		self.emailed_key = emailed_key

class Conversations(db.Model):
	__tablename__ = 'conversations'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	user = db.relationship('Users', backref='conversation')

	def __init__(self, user_id):
		self.user_id = user_id

	def serialize(self):
		return {
			'id': self.id,
			'start_date': self.start_date
		}

class Messages(db.Model):
	__tablename__ = 'messages'
	id = db.Column(db.Integer, primary_key=True)
	conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'))
	text = db.Column(db.String(255), nullable=False)
	name = db.Column(db.String(20), nullable=False)
	timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	conversation = db.relationship('Conversations', backref='message')

	def __init__(self, conversation_id, text, name):
		self.conversation_id = conversation_id
		self.text = text
		self.name = name
	
	def serialize(self):
		return {
			'timestamp': self.timestamp,
			'name': self.name,
			'text': self.text
		}

def create_app():
	app = Flask(__name__)
	app.config.from_pyfile('app.cfg')
	db.init_app(app)
	return app
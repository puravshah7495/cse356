from flask import Flask, render_template, request, jsonify
import time
import random

from models import Users, VerifyKeys, Conversations, Messages, db, create_app
from views.eliza import elizaModule
from views.account import accountModule

app = create_app()
app.app_context().push()
db.create_all(app=app)
app.register_blueprint(elizaModule)
app.register_blueprint(accountModule)

with app.app_context():
	db.create_all()

@app.route("/")
def hello():
	return render_template('index.html')

if __name__ == "__main__":
	app.run()

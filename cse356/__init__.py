from flask import Flask, render_template, request, jsonify
import time
import random

from views.eliza import elizaModule
from views.account import accountModule

app = Flask(__name__)
app.register_blueprint(elizaModule)
app.register_blueprint(accountModule)

@app.route("/")
def hello():
	return render_template('index.html')

if __name__ == "__main__":
	app.run()

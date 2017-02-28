from flask import Flask, render_template, request, jsonify
import time
import random

from views.eliza import elizaModule

app = Flask(__name__)
app.register_blueprint(elizaModule)

@app.route("/")
def hello():
	return render_template('index.html')

if __name__ == "__main__":
	app.run()

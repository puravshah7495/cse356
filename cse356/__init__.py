from flask import Flask, render_template, request, jsonify
import time
import random

app = Flask(__name__)

@app.route("/")
def hello():
	return render_template('index.html')

@app.route("/eliza/", methods=['GET', 'POST'])
def eliza():
	if request.method == 'GET':
		return render_template('eliza.html')
	else:
		name = request.form['name']
		date = time.strftime("%m/%d/%Y")
		return render_template('eliza.html',response="Hello %s, today's date is %s" % (name, date))

@app.route('/eliza/DOCTOR/', methods=['POST'])
def doctor():
	phrases = ['I don\'t understand, please elaborate.', 'That\'s interesting', 'Tell me more about that',
				'Are you sure?', 'How does that make you feel?', 'And why is that?']

	print request.values
	if len(request.values) != 0:
		print "here1"
		if 'human' not in request.values:
			print "here"
			return jsonify(eliza="")
		humanInput = request.values['human']
		response = "And how does that make you feel?"
		if not humanInput:
			response = "Please say something"
		elif humanInput.find('you') != -1:
			response = "We're here to talk about you not me"
		elif humanInput.find('I feel') != -1:
			response = "And why do you feel that way?"
		else:
			response = random.choice(phrases)

		return jsonify(eliza=response)
	else:
		return jsonify(eliza="")

if __name__ == "__main__":
	app.run()

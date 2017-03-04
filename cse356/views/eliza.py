from flask import Blueprint, render_template, request, jsonify, session
from cse356.models import db, Messages, Conversations, Users
from cse356.views.account import getRequestData
import time
import random

elizaModule = Blueprint('elizaModule', __name__)

@elizaModule.route("/eliza/", methods=['GET', 'POST'])
def eliza():
	if request.method == 'GET':
		return render_template('eliza/eliza.html')
	else:
		name = request.form['name']
		date = time.strftime("%m/%d/%Y")
		return render_template('eliza/eliza.html',response="Hello %s, today's date is %s" % (name, date))

@elizaModule.route('/DOCTOR', methods=['POST'])
@elizaModule.route('/eliza/DOCTOR/', methods=['POST'])
def doctor():
	username = None
	conversationId = None
	if session.get('loggedIn'):
		username = session.get('username')
		user = Users.query.filter_by(username=username).first()
		if session.get('elizaSession'):
			conversationId = session.get('elizaSession')
		else:
			conversation = Conversations(user.id)
			db.session.add(conversation)
			db.session.commit()
			session['elizaSession'] = conversation.id
			conversationId = conversation.id

	phrases = ['I don\'t understand, please elaborate.', 
				'That\'s interesting', 
				'Tell me more about that',
				'Are you sure?', 
				"Can you elaborate on that?",
				"Oh, I see.",
				"And how does that make you feel?",
				"What does that make you feel?",
				"Why?",
				"What else?",
				"What about it?",
				"That sounds interesting.",
				"Can you tell me more?"]
	
	question = ["What do you think the answer is?",
					"I'll be asking the questions here.",
					"What is the answer?",
					"I can't answer that.",
					"Find the answer yourself.",
					"Think about your question carefully.",
					"Why do you ask that?"]

	you =  ["I'm more interested in you.",
				"Tell me more about yourself instead.",
				"I'm here for you.",
				"I'm not that important here.",
				"Let's talk more about yourself.",
				"Tell me more about yourself."]
	data = getRequestData(request)
	if len(data) != 0:
		if 'human' not in data:
			return jsonify(eliza="")
		humanInput = data['human']
		response = "And how does that make you feel?"
		if not humanInput:
			response = "Please say something"
		elif humanInput.find('you') != -1:
			random.choice(you)
		elif humanInput.find('I feel') != -1:
			response = "And why do you feel that way?"
		elif humanInput.find('?') != -1:
			response = random.choice(question)
		else:
			response = random.choice(phrases)
		if session.get('loggedIn'):
			print user
			userMessage = Messages(conversationId, humanInput, username)
			elizaMessage = Messages(conversationId, response, 'Eliza')
			db.session.add(userMessage)
			db.session.add(elizaMessage)
			db.session.commit()
		return jsonify(eliza=response)
	else:
		return jsonify(eliza="")
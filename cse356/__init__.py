from flask import Flask, render_template, request, jsonify
import time
import random
import pika

from models import Users, VerifyKeys, Conversations, Messages, db, create_app
from views.eliza import elizaModule
from views.account import accountModule, getRequestData

app = create_app()
app.app_context().push()
db.create_all(app=app)
app.register_blueprint(elizaModule)
app.register_blueprint(accountModule)

with app.app_context():
	db.create_all()

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

def callback(ch, method, properties, body):
	return jsonify({'msg':body})

@app.route("/")
def hello():
	return render_template('index.html')

@app.route("/listen", methods=['POST'])
def createQueue():
	data = getRequestData(request)
	channel.exchange_declare(exchange='hw3', type='direct')
	keys = [str(x) for x in data['keys']]
	queue = channel.queue_declare(exclusive=True)
	queueName = queue.method.queue
	for key in keys:
		channel.queue_bind(exchange='hw3', queue=queueName, routing_key=key)
		channel.basic_consume(callback, queue=queueName, no_ack=True)
	return jsonify({'success':True})

@app.route('/speak', methods=['POST'])
def sendMessage():
	data = getRequestData(request)
	key = data['key']
	message = data['msg']
	channel.exchange_declare(exchange='hw3', type='direct')
	channel.basic_publish(exchange='hw3', routing_key=key, body=message)
	return jsonify({'msg':message})

if __name__ == "__main__":
	app.run()

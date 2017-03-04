from flask import Blueprint, render_template, request, redirect, session, make_response, jsonify
import json
from cse356.models import db, Users, VerifyKeys, Messages, Conversations

accountModule = Blueprint("accountModule",__name__)

def getRequestData(request):
    if request.get_json():
        return request.get_json()
    else:
        return request.values

def verifyUser(user, verification):
    user.verified = True
    if verification:
        db.session.delete(verification)
    db.session.commit()


@accountModule.route('/adduser', methods=['POST'])
def createAccount():
    data = getRequestData(request)
    if 'username' not in data or 'password' not in data or 'email' not in data:
        return jsonify({'status':'ERROR'})
    username = data['username']
    password = data['password']
    email = data['email']
    newUser = Users(username, password, email)
    db.session.add(newUser)
    db.session.commit()

    return jsonify({'status':'OK'}) 

@accountModule.route('/verify', methods=['POST'])
def verify():
    data = getRequestData(request)
    email = data['email']
    key = data['key']
    user = Users.query.filter_by(email=email).first()
    verification = VerifyKeys.query.join(Users, Users.id==VerifyKeys.user_id).filter(Users.email == email).filter(VerifyKeys.emailed_key == key).first()
    if key == 'abracadabra' or verification:
        verifyUser(user, verification)
        return jsonify({'status':'OK'})    
    return jsonify({'status':'ERROR'})   

@accountModule.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('account/login.html')
    else:
        data = getRequestData(request)
        if 'username' not in data or 'password' not in data:
            return jsonify({'status':'ERROR'})
        username = data['username']
        password = data['password']
        if not username or not password:
            return jsonify({'status': 'ERROR'})
        user = Users.query.filter_by(username=username, password=password).first()
        if user:
            session['loggedIn'] = True
            session['username'] = user.username
            return jsonify({'status':'OK'}) 
        else:
            return jsonify({'status':'ERROR'})

@accountModule.route('/logout', methods=['POST'])
def logout():
    if session.get('loggedIn'):
        userId = session.get('userId')
        session.pop('userId',None)
        session.pop('loggedIn', False)
        session.pop('elizaSession',None)
        return jsonify({'status':'OK'}) 
    else:
        return jsonify({'status':'ERROR'}) 

@accountModule.route('/listconv', methods=['POST'])
def listConv():
    if session.get('loggedIn'):
        username = session.get('username')
        user = Users.query.filter_by(username=username).first()
        conv = Conversations.query.filter_by(user_id = user.id).all()
        convList = [x.serialize() for x in conv]
        return jsonify({'status':'OK', "conversations":convList})
    else:
        return jsonify({'status':'ERROR'})

@accountModule.route('/getconv', methods=['POST'])
def getConv():
    if session.get('loggedIn'):
    	data = getRequestData(request)
    	if 'id' not in data:
        	return jsonify({'status':'ERROR'})
    	id = data['id']
    	messages = Messages.query.filter_by(conversation_id = id).all()
        messageList = [x.serialize() for x in messages]
    	return jsonify({'status':'OK', 'conversation':messageList})
    else:
    	return jsonify({'status':'ERROR'})
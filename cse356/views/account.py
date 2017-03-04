from flask import Blueprint, render_template, request, redirect, session, make_response, jsonify
import json
from cse356.models import db, User, VerifyKeys, Messages, Conversations

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
    newUser = User(username, password, email)
    db.session.add(newUser)
    db.session.commit()

    return jsonify({'status':'OK'}) 

@accountModule.route('/verify', methods=['POST'])
def verify():
    data = getRequestData(request)
    email = data['email']
    key = data['key']
    user = User.query.filter_by(email=email).first()
    verification = VerifyKeys.query.join(User, User.id==VerifyKeys.user_id).filter(User.email == email).filter(VerifyKeys.emailed_key == key).first()
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
        user = User.query.filter_by(username=username, password=password).first()
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
        return jsonify({'status':'OK'}) 
    else:
        return jsonify({'status':'ERROR'}) 

@accountModule.route('/listconv', methods=['POST'])
def listConv():
    if session.get('loggedIn'):
        userId = session.get('userId')
        conv = Conversations.query.filter_by(user_id = userId).all()
        return jsonify({'status':'OK', "conversations":conv})
    else:
        return jsonify({'status':'ERROR'})

@accountModule.route('/getconv', methods=['POST'])
def getConv():
    return None
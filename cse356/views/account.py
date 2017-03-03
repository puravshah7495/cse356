from flask import Blueprint, render_template, request, redirect, session, make_response, jsonify
from cse356.models import db, User, VerifyKeys, Messages, Conversations

accountModule = Blueprint("accountModule",__name__)

def verifyUser(user, verification):
    user.verified = True
    if verification:
        db.session.delete(verification)
        db.session.commit()


@accountModule.route('/adduser', methods=['POST'])
def createAccount():
    username = request.values['username']
    password = request.values['password']
    email = request.values['email']
    newUser = User(username, password, email)
    db.session.add(newUser)
    db.session.commit()

    return jsonify({'status':'OK'}) 

@accountModule.route('/verify', methods=['POST'])
def verify():
    email = request.values['email']
    key = request.values['key']
    user = User.query.filter_by(email=email).first()
    verification = VerifyKeys.query.join(User, User.id==VerifyKeys.user_id).filter(User.email == email).filter(VerifyKeys.emailed_key == key).first()
    if key == 'abracadabra' or verification:
        verifyUser(user, verification)
        return jsonify({'status':'OK'})       

@accountModule.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('account/login.html')
    else:
        username = request.values['username']
        password = request.values['password']
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

@accountModule.route('/listconv')
def listConv():
    return None

@accountModule.route('/getconv')
def getConv():
    return None
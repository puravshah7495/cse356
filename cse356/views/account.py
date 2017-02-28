from flask import Blueprint, render_template, request

accountModule = Blueprint("accountModule",__name__)

@accountModule.route('/adduser', methods=['POST'])
def createAccount():
    return None

@accountModule.route('/verify', methods=['PUT'])
def verify():
    return None

@accountModule.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('account/login.html')

@accountModule.route('/logout')
def logout():
    return None

@accountModule.route('/listconv')
def listConv():
    return None

@accountModule.route('/getconv')
def getConv():
    return None
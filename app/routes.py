from app import app
from flask import request
from app.controller import DosenController 
from app.controller import UserController
from flask_swagger_ui import get_swaggerui_blueprint


@app.route('/')
def index():
    return "<b>Hello</b>"

@app.route('/dosen', methods=['GET', 'POST'])
def dosens():
    if request.method == 'GET':
        return DosenController.index()
    else:
        return DosenController.save()

@app.route('/createadmin', methods=['POST'])
def admins():
    return UserController.buatAdmin()

@app.route('/dosen/<id>', methods=['GET', 'PUT', 'DELETE'])
def dosenDetail(id):
    if request.method == 'GET':
        return DosenController.detail(id)
    elif request.method == 'PUT':
        return DosenController.ubah(id)
    else:
        return DosenController.hapus(id)

@app.route('/login', methods=['POST'])
def logins():
    return UserController.login()

# SWAGGER_URL = '/api/docs'
# API_URL = '/static/openapi.json'
# swaggerui_blueprint = get_swaggerui_blueprint(
#     SWAGGER_URL, 
#     API_URL,
#     config={
#         'app-name' : 'syaiba-Python3-Flask-Rest-Boilerplate'
#     })
# app.register_blueprint(swaggerui_blueprint)
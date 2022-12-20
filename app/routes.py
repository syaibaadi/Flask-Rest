from app import app, response
from flask import request, make_response, send_from_directory, render_template
from app.controller import DosenController 
from app.controller import UserController
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

@app.route('/')
def index():
    return "<b>Hello</b>"

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return response.success(current_user, 'Sukses')


@app.route('/dosen', methods=['GET', 'POST'])
def dosens():
    if request.method == 'GET':
        return DosenController.index()
    else:
        return DosenController.save()

@app.route('/api/docs')
def get_docs():
    print('sending docs')
    return render_template('swaggerui.html')


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

@app.route('/file-upload', methods=['POST'])
def uploads():
    return UserController.upload()

@app.route('/api/dosen/page', methods=['GET'])
def pagination():
    return DosenController.paginate()
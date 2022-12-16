from app.model.user import User

from app import response, app, db
from flask import request
from flask_jwt_extended import *
import datetime

def buatAdmin():
    try:
        nama = request.form.get('nama')
        email = request.form.get('email')
        password = request.form.get('password')

        users = User(nama=nama, email=email)
        users.setPassword(password)
        db.session.add(users)
        db.session.commit()
        
        return response.success('', 'Data Admin Berhasil Ditambahkan')
    except Exception as e:
        print(e)

def singleObject(data):
    data = {
        'id' : data.id,
        'nama' : data.nama,
        'email' : data.email,
    }

    return data

def login():
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user:
            return response.badRequest([], 'Data Tidak Ditemukan')
        
        if not user.checkPassword(password):
            return response.badRequest([], 'Data Password Salah')

        data = singleObject(user)

        expires = datetime.timedelta(days=7)
        expires_refresh = datetime.timedelta(days=7)

        access_token = create_access_token(data, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(data, expires_delta=expires_refresh)

        return response.success({
            "data":data,
            "access_token" : access_token,
            "refresh_token" : refresh_token
        }, "Sukses Login")

    except Exception as e:
        print(e)
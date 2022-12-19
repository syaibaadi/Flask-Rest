from app.model.dosen import Dosen
from app.model.mahasiswa import Mahasiswa

from app import response, app, db
from flask import request, jsonify
import math

def index():
    try:
        dosen = Dosen.query.all()
        data = formatarray(dosen)
        return response.success(data, "Success")
        
    except Exception as e:
        print(e)


def formatarray(datas):
    array = []

    for i in datas:
        array.append(singleObject(i))

    return array

def singleObject(data):
    data = {
        'id' : data.id,
        'nidn' : data.nidn,
        'nama' : data.nama,
        'alamat' : data.alamat,
        'phone' : data.phone,
    }

    return data

def detail(id):
    try:
        dosen = Dosen.query.filter_by(id=id).first()
        mahasiswa = Mahasiswa.query.filter((Mahasiswa.dosen_satu == id) | (Mahasiswa.dosen_dua == id))


        if not dosen:
            return response.badRequest([], 'Tidak ada Data Dosen')

        datamahasiswa = formatMahasiswa(mahasiswa)

        data = singleDetailMahasiswa(dosen, datamahasiswa)

        return response.success(data, "Success")
    except Exception as e:
        print(e)
        
def singleDetailMahasiswa(dosen, mahasiswa):
    data = {
        'id' : dosen.id,
        'nidn' : dosen.nidn,
        'nama' : dosen.nama,
        'phone' : dosen.phone,
        'mahasiswa': mahasiswa
    }
    return data

def singleMahasiswa(mahasiswa):
    data = {
        'id' : mahasiswa.id,
        'nim': mahasiswa.nim,
        'nama' : mahasiswa.nama,
        'alamat' : mahasiswa.alamat,
        'phone' : mahasiswa.phone
    }
    return data

def formatMahasiswa(data):
    array = []

    for i in data:
        array.append(singleMahasiswa(i))
    return array

def save():
    try:
        nidn = request.form.get('nidn')
        nama = request.form.get('nama')
        alamat = request.form.get('alamat')
        phone = request.form.get('phone')

        dosens = Dosen(nidn=nidn, nama=nama, alamat=alamat, phone=phone)
        db.session.add(dosens)
        db.session.commit()
        
        return response.success('', 'Data Berhasil Ditambahkan')
    except Exception as e:
        print(e)

def ubah(id):
    try:
        nidn = request.form.get('nidn')
        nama = request.form.get('nama')
        alamat = request.form.get('alamat')
        phone = request.form.get('phone')

        input = [
            {
                'nidn': nidn,
                'nama' : nama,
                'alamat': alamat,
                'phone': phone
            }
        ]

        dosen = Dosen.query.filter_by(id=id).first()

        dosen.nidn = nidn
        dosen.nama = nama
        dosen.alamat = alamat
        dosen.phone = phone

        db.session.commit()

        return response.success(input, 'Data Berhasil Diubah')
    except Exception as e:
        print(e)

def hapus(id):
    try:
        dosen = Dosen.query.filter_by(id=id).first()
        if not dosen:
            return response.badRequest([], "Data Kosong")
        
        db.session.delete(dosen)
        db.session.commit()

        return response.success('', 'Berhasil Menghapus Data')
    except Exception as e:
        print(e)

#Fungsi Pagination
def get_pagination(clss, url, start, limit):
    results = clss.query.all()
    data = formatarray(results)
    count = len(data)

    obj = {}

    if count < start:
        obj['success'] = False
        obj['message'] = "Page melebihi batas limit data"
        return obj
    else:
        obj['success']=True
        obj['start_page']=start
        obj['per_page']=limit
        obj['total_data']=count
        obj['total_page']=math.ceil(count/limit)

        if start == 1:
            obj['previous']=''
        else:
            start_copy = max(1, start-limit)
            limit_copy = start - 1
            obj['previous']=url + '?start=%d&limit=%d' % (start_copy, limit)

        if start + limit > count:
            obj['next']=''
        else:
            start_copy = start + limit
            obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
        
        obj['results'] = data[(start - 1) : (start - 1 + limit)]
        return obj

def paginate():
    start = request.args.get('start')
    limit = request.args.get('limit')
    try:
        if start == None or limit == None:
            return jsonify(get_pagination(
                Dosen, 
                'http://127.0.0.1:5000/api/dosen/page', 
                start = request.args.get('start', 1), 
                limit = request.args.get('limit', 3)
            ))
        else:
            return jsonify(get_pagination(
            Dosen, 
            'http://127.0.0.1:5000/api/dosen/page', 
            start = int(start),
            limit = int(limit)
            ))
    except Exception as e:
        print(e)
from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(30), index=True, unique=True, nullable=False)
    passw = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return '<User {}>'.format(self.name)
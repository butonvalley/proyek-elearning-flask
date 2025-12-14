import uuid
from configs.db import db

class MataKuliah(db.Model):
    __tablename__ = "matakuliah"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))

    kode = db.Column(db.String(10), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    sks = db.Column(db.Integer, nullable=False)
    dosen_id = db.Column(db.String, db.ForeignKey("dosen.id"))
    kelas = db.relationship("Kelas", backref="matakuliah")

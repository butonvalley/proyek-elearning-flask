
import uuid
from configs.db import db

class Kelas(db.Model):
    __tablename__ = "kelas"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))

    nama = db.Column(db.String(50))
    semester = db.Column(db.String(10))
    tahun_ajaran = db.Column(db.String(20))
    matakuliah_id = db.Column(db.String, db.ForeignKey("matakuliah.id"))

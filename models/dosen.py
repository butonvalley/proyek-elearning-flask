import uuid
from configs.db import db

class Dosen(db.Model):
    __tablename__ = "dosen"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, db.ForeignKey("users.id"), unique=True, nullable=False)  # optional
    nidn = db.Column(db.String(20), unique=True, nullable=False)   
    user = db.relationship("User", backref=db.backref("dosen", uselist=False))  # optional
    matakuliah = db.relationship("MataKuliah", backref="dosen", cascade="all, delete-orphan")

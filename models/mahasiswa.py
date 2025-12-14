
import uuid
from configs.db import db

class Mahasiswa(db.Model):
    __tablename__ = "mahasiswa"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, db.ForeignKey("users.id"), unique=True, nullable=False) 
    user = db.relationship("User", backref=db.backref("mahasiswa", uselist=False)) 
    nim = db.Column(db.String(20), unique=True, nullable=False)
    alamat = db.Column(db.String(100),nullable=True)
    angkatan = db.Column(db.Integer)

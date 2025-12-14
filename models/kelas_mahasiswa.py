import uuid
from configs.db import db

class KelasMahasiswa(db.Model):
    __tablename__ = "kelas_mahasiswa"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))

    kelas_id = db.Column(db.String, db.ForeignKey("kelas.id"))
    mahasiswa_id = db.Column(db.String, db.ForeignKey("mahasiswa.id"))
    nilai_akhir = db.Column(db.Float)
    status = db.Column(db.String(20), default="aktif")

    # Relationship
    mahasiswa = db.relationship("Mahasiswa", backref="kelas_mahasiswa")
    kelas = db.relationship("Kelas", backref="kelas_mahasiswa")
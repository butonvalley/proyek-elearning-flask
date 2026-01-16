import uuid
from configs.db import db

class PenilaianKelas(db.Model):
    __tablename__ = "penilaian_kelas"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    kelas_id = db.Column(db.String, db.ForeignKey("kelas.id"), nullable=False, unique=True)

    # Range Nilai
    nilai_a_min = db.Column(db.Float, nullable=False)
    nilai_b_min = db.Column(db.Float, nullable=False)
    nilai_c_min = db.Column(db.Float, nullable=False)
    nilai_d_min = db.Column(db.Float, nullable=False)
    nilai_e_min = db.Column(db.Float, nullable=False, default=0)

    kelas = db.relationship("Kelas", backref=db.backref("penilaian", uselist=False))

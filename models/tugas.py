
from datetime import datetime, timezone
import uuid

from configs.db import db

class Tugas(db.Model):
    __tablename__ = "tugas"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    kelas_id = db.Column(db.String, db.ForeignKey("kelas.id"), nullable=False)
    dosen_id = db.Column(db.String, db.ForeignKey("dosen.id"), nullable=False)

    judul = db.Column(db.String(150), nullable=False)
    deskripsi = db.Column(db.Text)
    file_tugas = db.Column(db.String(255))
    deadline = db.Column(db.DateTime(timezone=True))

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    kelas = db.relationship("Kelas", backref="daftar_tugas")
    jawaban_mahasiswa = db.relationship(
        "TugasMahasiswa",
        back_populates="tugas",
        cascade="all, delete-orphan"
    )

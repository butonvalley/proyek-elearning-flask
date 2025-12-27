from datetime import datetime, timezone

import uuid
from configs.db import db


class TugasMahasiswa(db.Model):
    __tablename__ = "tugas_mahasiswa"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tugas_id = db.Column(db.String, db.ForeignKey("tugas.id"), nullable=False)
    mahasiswa_id = db.Column(db.String, db.ForeignKey("mahasiswa.id"), nullable=False)

    file_jawaban = db.Column(db.String(255), nullable=False)
    nilai = db.Column(db.Float)
    dikumpulkan_pada = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    tugas = db.relationship("Tugas", back_populates="jawaban_mahasiswa")
    mahasiswa = db.relationship("Mahasiswa", backref="jawaban_tugas")

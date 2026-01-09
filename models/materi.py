
from datetime import datetime, timezone
import uuid

from configs.db import db
import uuid
from datetime import datetime
from configs.db import db

class Materi(db.Model):
    __tablename__ = "materi"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    kelas_id = db.Column(db.String, db.ForeignKey("kelas.id"), nullable=False)
    dosen_id = db.Column(db.String, db.ForeignKey("dosen.id"), nullable=False)

    judul = db.Column(db.String(150), nullable=False)
    deskripsi = db.Column(db.Text)
    file = db.Column(db.String(255))  # bisa file PDF, video, dll
    link_eksternal = db.Column(db.String(255))  # bisa file PDF, video, dll
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    kelas = db.relationship("Kelas", backref="materi")
    dosen = db.relationship("Dosen", backref="materi")

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from datetime import datetime, timezone
from app.extensions import Base

class Football(Base):
    __tablename__ = "football_clubs" # Ubah nama tabel

    id = Column(Integer, primary_key=True)
    name = Column(Text) # Sebelumnya 'text'
    league = Column(String(100)) # Tambahkan kolom liga
    request_id = Column(Integer, ForeignKey("requests.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey # <-- Tambahkan String di sini
from datetime import datetime, timezone
from app.extensions import Base

class Football(Base):
    __tablename__ = "football_clubs"

    id = Column(Integer, primary_key=True)
    name = Column(Text) 
    league = Column(String(100)) # Sekarang String sudah dikenali
    request_id = Column(Integer, ForeignKey("requests.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
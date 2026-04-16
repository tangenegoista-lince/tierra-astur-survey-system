from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.models.base import Base

class Survey(Base):
    __tablename__ = "surveys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    card_image_url = Column(String, nullable=False)
    ocr_raw_text = Column(Text, nullable=True)
    processed_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(String(20), nullable=False, server_default='pending')
    validation_score = Column(Float, nullable=True)
    batch_id = Column(UUID(as_uuid=True), ForeignKey("processing_batches.id"), nullable=True)
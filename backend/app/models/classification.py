from sqlalchemy import Column, String, DateTime, UUID, Boolean, Float, Text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.sql import func
import uuid
from ..database import Base

class Classification(Base):
    __tablename__ = "classifications"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_id = Column(PostgresUUID(as_uuid=True), nullable=False, index=True)
    classification_type = Column(String, nullable=False)  # 'business' or 'personal'
    confidence_score = Column(Float)
    llm_reasoning = Column(Text)
    user_override = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Classification(id={self.id}, type={self.classification_type}, confidence={self.confidence_score})>" 
from sqlalchemy import Column, String, DateTime, UUID, Boolean, Float, Text, Date, Numeric
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.sql import func
import uuid
from ..database import Base

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PostgresUUID(as_uuid=True), nullable=False, index=True)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default='USD')
    merchant = Column(String)
    category = Column(String)
    is_business_expense = Column(Boolean)
    confidence_score = Column(Float)
    llm_reasoning = Column(Text)
    manually_overridden = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, description={self.description}, amount={self.amount})>" 
from sqlalchemy import Column, DateTime, Float, Integer, String, UniqueConstraint
from app.db.base import Base


class CostRecord(Base):
    __tablename__ = "cost_records"

    id = Column(Integer, primary_key=True, index=True)
    service = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint("service", "period_start", name="uq_service_period_start"),
    )
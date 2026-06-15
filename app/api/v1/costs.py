from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.cost import CostRecord
from app.services.aws_cost import run_ingest
from app.core.config import settings

router = APIRouter()


@router.post("/costs/ingest")
def ingest_costs(db: Session = Depends(get_db)):
    return run_ingest(db)


@router.get("/costs")
def get_costs(
    service: Optional[str] = Query(None),
    start: Optional[date] = Query(None),
    end: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(CostRecord)
    if service:
        query = query.filter(CostRecord.service == service)
    if start:
        query = query.filter(CostRecord.period_start >= start)
    if end:
        query = query.filter(CostRecord.period_start <= end)
    records = query.order_by(CostRecord.period_start.desc()).all()
    return [
        {
            "id": r.id,
            "service": r.service,
            "cost": r.cost,
            "currency": r.currency,
            "period_start": r.period_start.date().isoformat(),
            "period_end": r.period_end.date().isoformat(),
        }
        for r in records
    ]


@router.get("/costs/summary")
def get_summary(db: Session = Depends(get_db)):
    rows = (
        db.query(CostRecord.service, func.sum(CostRecord.cost).label("total"))
        .group_by(CostRecord.service)
        .order_by(func.sum(CostRecord.cost).desc())
        .all()
    )
    total = sum(r.total for r in rows)
    return {
        "total_usd": round(total, 4),
        "threshold_usd": settings.aws_cost_alert_threshold,
        "alert": total > settings.aws_cost_alert_threshold,
        "by_service": [
            {"service": r.service, "total_usd": round(r.total, 4)}
            for r in rows
        ],
    }

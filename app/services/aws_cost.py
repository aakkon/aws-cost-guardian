import boto3
from datetime import date, datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.core.config import settings
from app.models.cost import CostRecord


def get_aws_costs():
    session_kwargs = {}
    if settings.aws_profile:
        session_kwargs["profile_name"] = settings.aws_profile

    session = boto3.Session(**session_kwargs, region_name=settings.aws_region)
    client = session.client("ce")

    today = date.today()
    start = today.replace(day=1).isoformat()
    end = today.isoformat()

    response = client.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end},
        Granularity="DAILY",
        Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
    )

    return response


def run_ingest(db: Session) -> dict:
    data = get_aws_costs()
    rows = []

    for result in data["ResultsByTime"]:
        period_start = datetime.fromisoformat(result["TimePeriod"]["Start"])
        period_end = datetime.fromisoformat(result["TimePeriod"]["End"])

        for group in result["Groups"]:
            rows.append({
                "service": group["Keys"][0],
                "cost": float(group["Metrics"]["UnblendedCost"]["Amount"]),
                "currency": group["Metrics"]["UnblendedCost"]["Unit"],
                "period_start": period_start,
                "period_end": period_end,
                "created_at": datetime.now(timezone.utc),
            })

    stmt = insert(CostRecord).values(rows)
    stmt = stmt.on_conflict_do_update(
        index_elements=["service", "period_start"],
        set_={"cost": stmt.excluded.cost, "created_at": stmt.excluded.created_at},
    )
    db.execute(stmt)
    db.commit()

    return {"upserted": len(rows), "periods": len(data["ResultsByTime"])}

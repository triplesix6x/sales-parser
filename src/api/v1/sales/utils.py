from core.models import Sale
from datetime import date


def sale_to_dict(sale: Sale) -> dict:
    return {
        "id": sale.id,
        "date": sale.date.isoformat(),
        "report": sale.report,
    }


def sale_from_dict(data: dict) -> Sale:
    return Sale(
        id=data["id"],
        date=date.fromisoformat(data["date"]),
        report=data["report"]
    )

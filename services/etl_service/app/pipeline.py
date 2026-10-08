from datetime import datetime
from decimal import Decimal

SOURCE_DATA = [
    {"customer": "  alice  ", "amount": "1200.50", "date": "2026-10-01"},
    {"customer": "BOB", "amount": "850.00", "date": "2026-10-02"},
    {"customer": "  charlie", "amount": "300.25", "date": "2026-10-03"},
    {"customer": "", "amount": "-10", "date": "invalid"},
]

def extract():
    return SOURCE_DATA.copy()

def transform(rows):
    output = []
    for row in rows:
        customer = row["customer"].strip().title()
        try:
            amount = Decimal(row["amount"])
            date = datetime.strptime(row["date"], "%Y-%m-%d").date()
        except Exception:
            continue

        if not customer or amount <= 0:
            continue

        status = "high_value" if amount >= 1000 else "normal"

        output.append({
            "customer": customer,
            "amount": amount,
            "sale_date": date,
            "status": status,
        })
    return output

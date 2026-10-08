from fastapi import FastAPI, Depends
from sqlalchemy import String, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column, Session
from .database import Base, engine, get_db
from .pipeline import extract, transform

class ETLRecord(Base):
    __tablename__ = "etl_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer: Mapped[str] = mapped_column(String(255))
    amount: Mapped[float] = mapped_column(Numeric(12, 2))
    sale_date: Mapped[object] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(50))

app = FastAPI(title="ETL Service", version="1.0.0")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"service": "etl", "status": "ok"}

@app.post("/etl/run")
def run_etl(db: Session = Depends(get_db)):
    extracted = extract()
    transformed = transform(extracted)

    db.query(ETLRecord).delete()

    for row in transformed:
        db.add(ETLRecord(**row))

    db.commit()

    return {
        "status": "completed",
        "extracted": len(extracted),
        "loaded": len(transformed),
        "records": [
            {
                "customer": row["customer"],
                "amount": str(row["amount"]),
                "sale_date": str(row["sale_date"]),
                "status": row["status"],
            }
            for row in transformed
        ],
    }

@app.get("/etl/status")
def etl_status(db: Session = Depends(get_db)):
    count = db.query(ETLRecord).count()
    return {"loaded_records": count}

import os
import time
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Ortam değişkenlerinden veritabanı bilgilerini okuyoruz (ConfigMap & Secret)
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "niqs_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Veritabanı Bağlantısı (Retry mekanizması ile)
engine = None
for _ in range(5):
    try:
        engine = create_engine(DATABASE_URL)
        engine.connect()
        break
    except Exception:
        time.sleep(2)

Base = declarative_base()

# Veritabanı Tablosu
class NetworkMetric(Base):
    __tablename__ = "network_metrics"

    id = Column(Integer, primary_key=True, index=True)
    device_name = Column(String, index=True)
    latency_ms = Column(Float)
    packet_loss_percent = Column(Float)

if engine:
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(title="NIQS Network Health Service")

# Sağlık Kontrolü (Liveness/Readiness Probes için)
@app.get("/healthz")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {"message": "NIQS Network Health Service v1.0 Calisiyor!"}

# Metrik Ekleme Endpoint'i
@app.post("/metrics/")
def create_metric(device_name: str, latency_ms: float, packet_loss_percent: float):
    if not engine:
        raise HTTPException(status_code=500, detail="Database baglantisi kurulamadi.")
    
    db = SessionLocal()
    metric = NetworkMetric(
        device_name=device_name,
        latency_ms=latency_ms,
        packet_loss_percent=packet_loss_percent
    )
    db.add(metric)
    db.commit()
    db.refresh(metric)
    db.close()
    return {"status": "success", "data": {"device_name": device_name, "latency_ms": latency_ms, "packet_loss_percent": packet_loss_percent}}

# Metrikleri Listeleme Endpoint'i
@app.get("/metrics/")
def get_metrics():
    if not engine:
        raise HTTPException(status_code=500, detail="Database baglantisi kurulamadi.")
    
    db = SessionLocal()
    metrics = db.query(NetworkMetric).all()
    db.close()
    return {"metrics": metrics}

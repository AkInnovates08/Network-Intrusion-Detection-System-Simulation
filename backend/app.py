import json
import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.db import init_db, insert_flow, insert_alert, rows, connect
from ids.feature_extractor import extract_network_features, validate_flow
from ids.rule_engine import analyze_flow
from ids.anomaly_detector import build_baseline, calculate_anomaly_score
from ids.risk_engine import calculate_risk_score, classify_risk
from ids.alert_engine import generate_alert


app = FastAPI(
    title="Network IDS Simulation API",
    version="1.1.0",
    description="Defensive synthetic network intrusion detection simulation API.",
)

# React/Vite runs on port 5173 while FastAPI runs on port 8000.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASELINE = []


class Flow(BaseModel):
    flow_id: str
    timestamp: str
    source_ip: str
    destination_ip: str
    source_port: int = Field(ge=0, le=65535)
    destination_port: int = Field(ge=0, le=65535)
    protocol: str
    packet_count: int = Field(ge=0)
    byte_count: int = Field(ge=0)
    duration_seconds: float = Field(ge=0)
    connection_count: int = Field(ge=0)
    failed_connection_count: int = Field(ge=0)
    syn_count: int = Field(ge=0)
    rst_count: int = Field(ge=0)
    unique_destination_ports: int = Field(default=1, ge=1)
    unique_destination_ips: int = Field(default=1, ge=1)


class Status(BaseModel):
    status: str


class Note(BaseModel):
    note: str = Field(min_length=1, max_length=2000)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"status": "ok", "service": "network-ids-simulation"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/api/flows")
def create_flow(flow: Flow):
    global BASELINE

    data = flow.model_dump()
    errors = validate_flow(data)
    if errors:
        raise HTTPException(status_code=422, detail=errors)

    features = extract_network_features(
        data,
        {
            "unique_destination_ports": data["unique_destination_ports"],
            "unique_destination_ips": data["unique_destination_ips"],
        },
    )

    baseline = (
        build_baseline(BASELINE)
        if len(BASELINE) >= 20
        else build_baseline([features] * 20)
    )

    anomaly = calculate_anomaly_score(features, baseline)
    rules = analyze_flow(features, data)
    risk = calculate_risk_score(rules, anomaly)
    classification = classify_risk(risk)

    data.update(
        {
            "risk_score": risk,
            "classification": classification,
        }
    )

    BASELINE.append(features)
    BASELINE[:] = BASELINE[-1000:]

    insert_flow(data)

    alert = generate_alert(data, rules, risk, anomaly)
    if alert:
        insert_alert(alert, data["flow_id"])

    return {
        "flow": data,
        "features": features,
        "rules": rules,
        "anomaly_score": anomaly,
        "risk_score": risk,
        "classification": classification,
        "alert": alert,
    }


@app.get("/api/flows")
def get_flows(limit: int = 100):
    return rows(
        "SELECT * FROM network_flows ORDER BY timestamp DESC LIMIT ?",
        (min(max(limit, 1), 1000),),
    )


@app.get("/api/flows/{flow_id}")
def get_flow(flow_id: str):
    result = rows(
        "SELECT * FROM network_flows WHERE flow_id=?",
        (flow_id,),
    )
    if not result:
        raise HTTPException(status_code=404, detail="Flow not found")
    return result[0]


@app.get("/api/alerts")
def get_alerts(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 100,
):
    query = "SELECT * FROM alerts WHERE 1=1"
    args = []

    if status:
        query += " AND status=?"
        args.append(status)

    if severity:
        query += " AND severity=?"
        args.append(severity)

    query += " ORDER BY created_at DESC LIMIT ?"
    args.append(min(max(limit, 1), 1000))

    return rows(query, args)


@app.get("/api/alerts/{alert_id}")
def get_alert(alert_id: str):
    result = rows(
        "SELECT * FROM alerts WHERE alert_id=?",
        (alert_id,),
    )
    if not result:
        raise HTTPException(status_code=404, detail="Alert not found")
    return result[0]


@app.put("/api/alerts/{alert_id}/status")
def update_status(alert_id: str, status_data: Status):
    allowed = {"NEW", "INVESTIGATING", "RESOLVED", "FALSE_POSITIVE"}

    if status_data.status not in allowed:
        raise HTTPException(status_code=400, detail="Invalid status")

    existing = rows(
        "SELECT alert_id FROM alerts WHERE alert_id=?",
        (alert_id,),
    )

    if not existing:
        raise HTTPException(status_code=404, detail="Alert not found")

    connection = connect()
    connection.execute(
        "UPDATE alerts SET status=? WHERE alert_id=?",
        (status_data.status, alert_id),
    )
    connection.commit()
    connection.close()

    return {
        "alert_id": alert_id,
        "status": status_data.status,
    }


@app.post("/api/alerts/{alert_id}/notes")
def add_note(alert_id: str, note_data: Note):
    if not rows(
        "SELECT alert_id FROM alerts WHERE alert_id=?",
        (alert_id,),
    ):
        raise HTTPException(status_code=404, detail="Alert not found")

    connection = connect()
    connection.execute(
        "INSERT INTO incident_notes(alert_id,note,created_at) VALUES(?,?,?)",
        (
            alert_id,
            note_data.note,
            datetime.datetime.now(datetime.timezone.utc).isoformat(),
        ),
    )
    connection.commit()
    connection.close()

    return {"status": "saved"}


@app.get("/api/alerts/{alert_id}/notes")
def get_notes(alert_id: str):
    if not rows(
        "SELECT alert_id FROM alerts WHERE alert_id=?",
        (alert_id,),
    ):
        raise HTTPException(status_code=404, detail="Alert not found")

    return rows(
        "SELECT note_id, alert_id, note, created_at "
        "FROM incident_notes WHERE alert_id=? ORDER BY created_at DESC",
        (alert_id,),
    )


@app.get("/api/dashboard/stats")
def dashboard_stats():
    flow_stats = rows(
        """
        SELECT
            COUNT(*) AS total_flows,
            COALESCE(SUM(CASE WHEN classification='NORMAL' THEN 1 ELSE 0 END), 0) AS normal,
            COALESCE(SUM(CASE WHEN classification!='NORMAL' THEN 1 ELSE 0 END), 0) AS suspicious,
            COALESCE(AVG(risk_score), 0) AS avg_risk
        FROM network_flows
        """
    )[0]

    alert_stats = rows(
        """
        SELECT
            COUNT(*) AS total_alerts,
            COALESCE(
                SUM(
                    CASE
                        WHEN status NOT IN ('RESOLVED', 'FALSE_POSITIVE')
                        THEN 1
                        ELSE 0
                    END
                ),
                0
            ) AS open_alerts,
            COALESCE(SUM(CASE WHEN severity='CRITICAL' THEN 1 ELSE 0 END), 0) AS critical
        FROM alerts
        """
    )[0]

    return {
        "total_flows": flow_stats["total_flows"],
        "normal": flow_stats["normal"],
        "suspicious": flow_stats["suspicious"],
        "avg_risk": flow_stats["avg_risk"],
        "total_alerts": alert_stats["total_alerts"],
        "open_alerts": alert_stats["open_alerts"],
        "critical": alert_stats["critical"],
    }


@app.get("/api/dashboard/traffic")
def traffic(limit: int = 500):
    return rows(
        """
        SELECT timestamp, protocol, destination_port,
               packet_count, byte_count, risk_score, classification
        FROM network_flows
        ORDER BY timestamp DESC
        LIMIT ?
        """,
        (min(max(limit, 1), 2000),),
    )


@app.get("/api/dashboard/alerts")
def alert_stats():
    return rows(
        "SELECT severity, COUNT(*) count "
        "FROM alerts GROUP BY severity ORDER BY count DESC"
    )


@app.get("/api/rules")
def rules():
    return rows("SELECT * FROM rules ORDER BY rule_id")

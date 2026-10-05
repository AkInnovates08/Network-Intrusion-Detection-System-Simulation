# Network Intrusion Detection System (IDS) Simulation

A defensive cybersecurity project that simulates network-flow monitoring, intrusion detection, anomaly detection, risk scoring, alert generation, incident investigation, and SOC-style security analytics using safe synthetic network traffic.

---

## Overview

The Network Intrusion Detection System (IDS) Simulation is an industry-oriented cybersecurity project designed to demonstrate how a Network-Based Intrusion Detection System can identify suspicious network behavior using synthetic network-flow records.

The project combines:

- Synthetic network traffic generation
- Network-flow feature extraction
- Signature and rule-based detection
- Statistical anomaly detection
- Optional machine learning detection
- Hybrid risk scoring
- Security alert generation
- Alert correlation
- SQLite security-event storage
- REST API services
- SOC-style dashboards
- Investigation filters
- Alert investigation workflow
- Analyst notes
- Incident management
- Automated testing
- Machine learning evaluation

All suspicious activity in this project is represented as synthetic data records. The simulator does not send attack packets, scan external systems, exploit vulnerabilities, or generate harmful network traffic.

---

## Project Objectives

The main objectives of this project are to:

1. Generate safe synthetic network-flow records.
2. Monitor and analyze network-flow information.
3. Extract security-relevant network features.
4. Detect suspicious patterns using configurable rules.
5. Detect statistical deviations from normal traffic baselines.
6. Optionally apply machine learning models.
7. Calculate a combined security risk score.
8. Generate and store security alerts.
9. Correlate related alerts.
10. Provide SOC-style security monitoring.
11. Provide analyst investigation capabilities.
12. Support incident status management.
13. Store analyst investigation notes.
14. Evaluate detection models using calculated metrics.
15. Demonstrate a complete defensive cybersecurity workflow.

---

# Cybersecurity Scope

This project is intentionally designed as a defensive cybersecurity simulation.

### Safe Data Sources

The project uses:

- Synthetic network-flow records
- Reserved documentation IP ranges
- Local SQLite storage
- Localhost APIs
- Authorized local simulation

Reserved documentation networks used by the simulator include:

```text
192.0.2.0/24
198.51.100.0/24
203.0.113.0/24
```

### No Real Attack Traffic

The project does not:

- Scan public networks
- Probe third-party systems
- Exploit vulnerabilities
- Perform credential attacks
- Generate DDoS traffic
- Flood network services
- Bypass security controls
- Steal credentials
- Attack external systems

Suspicious behavior is represented only through synthetic network-flow data.

---

# System Architecture

```text
                    Synthetic Traffic
                           |
                           v
                +----------------------+
                | Traffic Simulator    |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Flow Collector       |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Feature Extraction   |
                +----------+-----------+
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
        Rule Engine   Anomaly Engine   ML Model
             |             |             |
             +-------------+-------------+
                           |
                           v
                +----------------------+
                | Hybrid Risk Engine   |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Alert Engine         |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | SQLite Security DB   |
                +----------+-----------+
                           |
             +-------------+-------------+
             |                           |
             v                           v
     React SOC Console           Streamlit Dashboard
             |
             v
     Alert Investigation
             |
             v
      Analyst Notes
             |
             v
     Incident Resolution
```

---

# Detection Architecture

The project uses a hybrid detection approach.

```text
Signature Detection
        +
Anomaly Detection
        +
Optional Machine Learning
        =
Hybrid IDS
```

### Signature Detection

Detects predefined suspicious statistical patterns.

### Anomaly Detection

Compares observed network behavior against a statistical baseline.

### Machine Learning

Provides optional supervised and unsupervised detection.

### Hybrid Detection

Combines multiple detection signals into a final risk score.

---

# Network Flow Data

The synthetic dataset contains 5,000 network-flow records.

Main fields include:

| Field | Description |
|---|---|
| flow_id | Unique flow identifier |
| timestamp | Flow timestamp |
| source_ip | Synthetic source IP |
| destination_ip | Synthetic destination IP |
| source_port | Source port |
| destination_port | Destination port |
| protocol | TCP or UDP |
| packet_count | Number of packets |
| byte_count | Total bytes |
| duration_seconds | Flow duration |
| connection_count | Number of connections |
| failed_connection_count | Failed connection count |
| syn_count | SYN count |
| rst_count | RST count |
| average_packet_size | Average packet size |
| label | NORMAL or SUSPICIOUS |
| scenario_type | Synthetic traffic scenario |

Dataset location:

```text
data/network_traffic.csv
```

---

# Synthetic Traffic Scenarios

The dataset contains safe representations of multiple network behaviors.

### Normal Scenarios

```text
NORMAL_WEB
NORMAL_DNS
NORMAL_SSH
NORMAL_EMAIL
NORMAL_DATABASE
```

### Suspicious Scenarios

```text
HIGH_CONNECTION_RATE
REPEATED_FAILED_CONNECTIONS
MULTI_PORT_PROBING_PATTERN
SYN_HEAVY_PATTERN
UNUSUAL_PORT_ACTIVITY
HIGH_TRAFFIC_VOLUME
```

These are data-level representations and do not generate actual malicious network traffic.

---

# Feature Engineering

The IDS extracts security-relevant features such as:

```text
packet_count
byte_count
duration
bytes_per_second
packets_per_second
average_packet_size
connection_count
failed_connection_count
failure_ratio
syn_count
rst_count
syn_ratio
unique_destination_ports
unique_destination_ips
connection_rate
```

These features help identify:

- High connection activity
- Failed connection behavior
- Traffic-volume anomalies
- SYN-heavy behavior
- Port diversity
- Connection-rate deviations
- Unusual traffic patterns

---

# Signature-Based Detection

The rule engine contains configurable detection rules.

Current detection categories include:

### IDS-001

High Connection Rate

Detects unusually high connection activity.

### IDS-002

Repeated Failed Connections

Detects an unusually high number of failed connections.

### IDS-003

High Destination-Port Diversity

Detects unusual destination-port diversity.

### IDS-004

SYN-Heavy Behavior

Detects statistically unusual SYN activity.

### IDS-005

Unusual Service-Port Activity

Detects unexpected service-port behavior.

### IDS-006

High Traffic Volume

Detects abnormally large traffic volumes.

A rule match indicates suspicious behavior requiring investigation. It does not automatically prove malicious activity.

---

# Anomaly Detection

The anomaly detector establishes a baseline using normal network-flow behavior.

The general process is:

```text
Normal Baseline
       |
       v
Observe New Flow
       |
       v
Extract Features
       |
       v
Compare Against Baseline
       |
       v
Calculate Deviation
       |
       v
Anomaly Score
```

The anomaly score is represented on a:

```text
0 - 100
```

scale.

Higher scores represent larger deviations from the baseline.

Anomaly detection can identify unusual behavior that does not match predefined rules, but it can also produce false positives.

---

# Machine Learning Detection

The project optionally supports:

### Supervised Models

```text
Logistic Regression
Random Forest
```

### Unsupervised Model

```text
Isolation Forest
```

The supervised models are trained using labeled synthetic network-flow records.

The following metrics are calculated:

- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

Accuracy alone is not sufficient for security detection because false negatives and false positives can have significantly different operational consequences.

---

# Machine Learning Results

The models were evaluated using the generated synthetic dataset.

Example calculated results from the current dataset:

| Model | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Logistic Regression | 99.84% | 99.69% | 100% | 99.84% |
| Random Forest | 100% | 100% | 100% | 100% |

### Logistic Regression Confusion Matrix

```text
[[605, 2],
 [0, 643]]
```

### Random Forest Confusion Matrix

```text
[[607, 0],
 [0, 643]]
```

These results were calculated from the generated synthetic dataset and should not be interpreted as production IDS performance.

Synthetic datasets are generally easier to classify than real enterprise traffic.

---

# Hybrid Risk Scoring

The project combines detection signals into a final risk score.

When machine learning is enabled:

```text
Rule-Based Detection = 40%
Anomaly Detection    = 30%
Machine Learning     = 30%
```

When machine learning is disabled:

```text
Rule-Based Detection = 60%
Anomaly Detection    = 40%
```

The final risk score is:

```text
0 - 100
```

Risk classification:

| Score | Classification |
|---:|---|
| 0-20 | NORMAL |
| 21-40 | LOW RISK |
| 41-60 | SUSPICIOUS |
| 61-80 | HIGH RISK |
| 81-100 | CRITICAL INVESTIGATION |

These thresholds are project assumptions and should be calibrated using real organizational security data in a production environment.

---

# Alert Generation

When suspicious behavior is detected, the alert engine creates a security alert.

Alert information includes:

```text
alert_id
timestamp
source_ip
destination_ip
protocol
source_port
destination_port
rule_id
alert_type
severity
risk_score
description
status
```

Supported statuses:

```text
NEW
INVESTIGATING
RESOLVED
FALSE_POSITIVE
```

---

# Alert Correlation

The project supports basic alert correlation.

Related alerts can be grouped using:

```text
Source IP
Alert Type
Time Window
```

This helps reduce repetitive alerts and allows analysts to investigate related events as a group.

---

# SOC Dashboard

The project provides a SOC-style dashboard for monitoring network security activity.

The React dashboard provides:

- Total flows
- Normal traffic
- Suspicious traffic
- Open alerts
- Critical alerts
- Average risk
- Alerts by severity
- Recent alerts
- Automatic data refresh
- API connection status

---

# Investigation Console

The React frontend includes a dedicated investigation workflow.

## Investigation Filters

The investigation console supports:

```text
Status
Severity
Protocol
Alert Type
Time Range
Search
```

Example investigation:

```text
Status       = NEW
Severity     = HIGH
Protocol     = TCP
Alert Type   = High Connection Rate
Time Range   = Last 24 Hours
```

This allows a SOC analyst to narrow the alert queue quickly.

---

# Alert Queue

The Alert Queue displays security alerts including:

```text
Alert ID
Source IP
Destination IP
Alert Type
Severity
Risk Score
Status
```

Analysts can select an alert and open the investigation page.

---

# Alert Investigation

The investigation page provides security context including:

### Alert Details

```text
Alert ID
Timestamp
Alert Type
Rule ID
Severity
Status
Risk Score
Anomaly Score
ML Score
```

### Network Context

```text
Source IP
Source Port
Destination IP
Destination Port
Protocol
Flow ID
Classification
```

### Traffic Statistics

```text
Packet Count
Byte Count
Duration
Connection Count
Failed Connections
```

### Investigation Guidance

The analyst can review:

- Related logs
- Source identity
- Historical traffic baseline
- Authentication records
- Firewall records
- Endpoint telemetry
- Expected business behavior

---

# Incident Management

The investigation workflow supports:

```text
NEW
 |
 v
INVESTIGATING
 |
 +----------------+
 |                |
 v                v
RESOLVED     FALSE_POSITIVE
```

Analysts can add investigation notes and resolution information.

---

# Analyst Notes

The investigation console allows analysts to document their findings.

Example:

```text
Reviewed synthetic traffic pattern.
Connection rate exceeded the configured baseline.
Source requires further investigation.
```

Notes are stored in the database and associated with the relevant alert.

---

# Database

The project uses SQLite for local development and demonstration.

Main tables include:

```text
NETWORK_FLOWS
ALERTS
RULES
INCIDENT_NOTES
MODEL_RESULTS
```

## NETWORK_FLOWS

Stores network-flow information and detection results.

## ALERTS

Stores generated security alerts.

## RULES

Stores configurable IDS detection rules.

## INCIDENT_NOTES

Stores analyst investigation notes.

## MODEL_RESULTS

Stores optional machine-learning prediction results.

---

# REST API

The backend is implemented using FastAPI.

Base URL:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Flow Endpoints

### POST /api/flows

Submit a network-flow record for analysis.

### GET /api/flows

Retrieve network-flow records.

### GET /api/flows/{id}

Retrieve a specific flow.

---

## Alert Endpoints

### GET /api/alerts

Retrieve security alerts.

### GET /api/alerts/{id}

Retrieve a specific alert.

### PUT /api/alerts/{id}/status

Update alert status.

### POST /api/alerts/{id}/notes

Add analyst investigation notes.

### GET /api/alerts/{id}/notes

Retrieve analyst notes.

---

## Dashboard Endpoints

### GET /api/dashboard/stats

Returns dashboard statistics.

Example:

```json
{
  "total_flows": 1000,
  "normal": 403,
  "suspicious": 597,
  "avg_risk": 32.22,
  "total_alerts": 597,
  "open_alerts": 597,
  "critical": 0
}
```

### GET /api/dashboard/traffic

Returns traffic analytics.

### GET /api/dashboard/alerts

Returns alert analytics.

---

## Rule Endpoints

### GET /api/rules

Retrieve configured IDS rules.

### PUT /api/rules/{id}

Update a rule configuration.

---

# Project Structure

```text
Network-Intrusion-Detection-System-Simulation/
│
├── simulator/
│   ├── traffic_simulator.py
│   └── generate_dataset.py
│
├── ids/
│   ├── feature_extractor.py
│   ├── rule_engine.py
│   ├── anomaly_detector.py
│   ├── risk_engine.py
│   ├── alert_engine.py
│   └── correlation.py
│
├── ml/
│   ├── train_model.py
│   ├── predict.py
│   └── evaluate.py
│
├── backend/
│   ├── app.py
│   ├── db.py
│   └── seed.py
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   └── style.css
│   ├── package.json
│   └── index.html
│
├── data/
│   └── network_traffic.csv
│
├── models/
│
├── tests/
│   └── test_ids.py
│
├── screenshots/
├── docs/
├── reports/
│
├── dashboard.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# Technology Stack

## Backend

- Python
- FastAPI
- Uvicorn
- SQLite
- Pydantic

## Data Processing

- Pandas
- NumPy

## Machine Learning

- Scikit-learn

## Frontend

- React
- Vite
- Recharts
- CSS

## Dashboard

- Streamlit

## Testing

- Pytest

## Development Tools

- VS Code
- Git
- GitHub

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/AkInnovates08/Network-Intrusion-Detection-System-Simulation.git
```

Move into the project:

```bash
cd Network-Intrusion-Detection-System-Simulation
```

---

# 2. Create a Python Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

# 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

# 4. Generate Synthetic Dataset

Generate 5,000 network-flow records:

```bash
python -m simulator.generate_dataset --rows 5000
```

The generated dataset will be saved to:

```text
data/network_traffic.csv
```

---

# 5. Train Machine Learning Models

```bash
python -m ml.train_model
```

The training process calculates:

```text
Accuracy
Precision
Recall
F1 Score
Confusion Matrix
```

and stores trained model files under:

```text
models/
```

---

# 6. Start the FastAPI Backend

From the project root:

```bash
uvicorn backend.app:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# 7. Seed the Database

In another terminal:

```bash
python -m backend.seed
```

This loads synthetic network-flow records into the local security database.

---

# 8. Start the React SOC Console

Open another terminal:

```bash
cd frontend
```

Install frontend dependencies:

```bash
npm install
```

Start Vite:

```bash
npm run dev
```

Open:

```text
http://localhost:5173/
```

---

# 9. Start the Streamlit Dashboard

From the project root:

```bash
streamlit run dashboard.py
```

Open:

```text
http://localhost:8501
```

The Streamlit dashboard provides an additional security analytics interface.

---

# Running the Complete Simulation

Start the backend:

```bash
uvicorn backend.app:app --reload
```

Start React:

```bash
cd frontend
npm run dev
```

Start the synthetic traffic simulator:

```bash
cd ..
python -m simulator.traffic_simulator --mode mixed --speed slow
```

The simulator generates synthetic flow records only.

It does not transmit packets.

---

# Traffic Simulator

Normal mode:

```bash
python -m simulator.traffic_simulator --mode normal --speed slow
```

Mixed mode:

```bash
python -m simulator.traffic_simulator --mode mixed --speed slow
```

Fast mode:

```bash
python -m simulator.traffic_simulator --mode mixed --speed fast
```

The simulator produces JSON-style network-flow records.

Example:

```json
{
  "flow_id": "FLOW-000001",
  "timestamp": "2026-10-05T12:34:59.432753+00:00",
  "source_ip": "192.0.2.2",
  "destination_ip": "198.51.100.11",
  "source_port": 38773,
  "destination_port": 443,
  "protocol": "TCP",
  "packet_count": 38,
  "byte_count": 16921,
  "duration_seconds": 7.062,
  "connection_count": 3,
  "failed_connection_count": 0,
  "syn_count": 0,
  "rst_count": 1
}
```

---

# Testing

Run all automated tests:

```bash
pytest -v
```

Current project validation:

```text
32 tests passed
```

The test suite covers:

- Valid network flows
- Invalid IP addresses
- Invalid ports
- Unsupported protocols
- Zero duration
- High connection rate
- Failed connections
- Port diversity
- SYN-heavy behavior
- Unusual ports
- High traffic volume
- Feature extraction
- Risk scoring
- Classification
- Alert creation
- Missing fields
- Negative values
- Boundary conditions

---

# Testing Workflow

A recommended demonstration sequence is:

```text
1. Generate dataset
        |
        v
2. Start backend
        |
        v
3. Seed database
        |
        v
4. Start React dashboard
        |
        v
5. Start Streamlit dashboard
        |
        v
6. Generate synthetic traffic
        |
        v
7. Observe alerts
        |
        v
8. Open Alert Queue
        |
        v
9. Apply Investigation Filters
        |
        v
10. Open an alert
        |
        v
11. Start investigation
        |
        v
12. Add analyst note
        |
        v
13. Resolve or mark false positive
```

---

# False Positives

A false positive occurs when legitimate activity is incorrectly classified as suspicious.

Example:

```text
A legitimate backup system suddenly generates
unusually high traffic.
```

The IDS may detect the statistical deviation even though the activity is legitimate.

False positives are important because excessive alert volume can create analyst fatigue.

---

# False Negatives

A false negative occurs when suspicious behavior is incorrectly classified as normal.

False negatives are particularly important in security monitoring because undetected malicious activity may remain unnoticed.

Detection quality can be improved using:

- Better baselines
- Multiple detection techniques
- Threshold tuning
- Analyst feedback
- Contextual information
- Historical behavior

---

# Confusion Matrix

Machine learning evaluation uses:

### True Positive

Suspicious activity correctly detected.

### True Negative

Normal activity correctly classified as normal.

### False Positive

Normal activity incorrectly classified as suspicious.

### False Negative

Suspicious activity incorrectly classified as normal.

Security teams often pay close attention to recall because missing suspicious activity can be costly, while also managing false-positive volume so analysts are not overwhelmed.

---

# SOC Analyst Workflow

The project simulates a simplified SOC workflow:

```text
Network Event
      |
      v
IDS Detection
      |
      v
Alert
      |
      v
SOC Queue
      |
      v
Triage
      |
      v
Context Investigation
      |
      v
Severity Assessment
      |
      +-------------------+
      |                   |
      v                   v
  Escalate             Resolve
      |                   |
      +---------+---------+
                |
                v
          Documentation
```

---

# Investigation Process

A SOC analyst can investigate an alert by:

1. Reviewing the alert details.
2. Checking the source and destination.
3. Reviewing traffic statistics.
4. Examining the matched detection rule.
5. Reviewing the anomaly score.
6. Reviewing the ML score if available.
7. Comparing activity with the baseline.
8. Checking authorized security logs.
9. Reviewing firewall records.
10. Determining whether the activity is expected.
11. Documenting findings.
12. Resolving the incident or marking it as a false positive.

---

# IDS vs IPS

| IDS | IPS |
|---|---|
| Detects suspicious activity | Detects suspicious activity |
| Generates alerts | Can automatically prevent activity |
| Primarily monitoring | Prevention and enforcement |
| Does not automatically block | Can block or modify traffic |
| Supports investigation | Supports automated response |

This project intentionally implements an IDS simulation rather than an IPS.

The system detects and reports suspicious behavior without automatically blocking network traffic.

---

# Signature vs Anomaly Detection

| Feature | Signature-Based | Anomaly-Based |
|---|---|---|
| Detection method | Known patterns | Deviations from baseline |
| Explainability | High | Moderate |
| Unknown behavior | Limited | Better coverage |
| False positives | Often lower for precise rules | Can be higher |
| Speed | Usually fast | Depends on baseline/model |
| Main strength | Known behavior | Unusual behavior |

The project combines both approaches to provide broader detection coverage.

---

# Industry Relevance

IDS technology is commonly associated with security monitoring environments such as:

- Security Operations Centers
- Banks
- Cloud providers
- Enterprises
- Data centers
- Government organizations
- Universities
- E-commerce organizations
- Managed Security Service Providers

The project demonstrates skills relevant to roles such as:

- SOC Analyst
- Network Security Analyst
- Cybersecurity Analyst
- Security Engineer
- Incident Response Analyst
- Threat Detection Engineer
- Security Data Analyst

---

# MITRE ATT&CK Considerations

Network-security alerts can be mapped to MITRE ATT&CK techniques when sufficient evidence exists.

However, a statistical anomaly alone should not automatically be interpreted as a specific attack technique.

A proper mapping should consider:

- Detection evidence
- Network context
- Authentication information
- Endpoint telemetry
- Security logs
- Analyst investigation

ATT&CK mapping can help with:

- Detection documentation
- SOC investigation
- Threat hunting
- Security reporting

---

# SIEM Integration Concept

The generated alerts can conceptually be forwarded to a SIEM.

```text
IDS
 |
 v
JSON Alert
 |
 v
Log Forwarder / API
 |
 v
SIEM
 |
 v
Correlation
 |
 v
SOC Analyst
```

Example alert:

```json
{
  "alert_id": "ALT-1001",
  "source_ip": "192.0.2.15",
  "destination_ip": "198.51.100.20",
  "severity": "HIGH",
  "rule": "High Connection Rate",
  "risk_score": 78
}
```

No commercial SIEM is required for this project.

---

# Security and Privacy

Security monitoring data can be sensitive because it may contain information about:

- Internal systems
- IP addresses
- Network relationships
- Authentication behavior
- Security events
- Infrastructure patterns
- User activity

Recommended production security controls include:

- Authentication
- Authorization
- Least privilege
- HTTPS
- Secure secret management
- API rate limiting
- Log protection
- Audit logging
- Input validation
- Output sanitization
- Protected analyst notes
- Encrypted storage where appropriate

This student implementation uses synthetic data for safe development and demonstration.

---

# Project Limitations

This project is a simulation and does not represent a production enterprise IDS.

Current limitations include:

- Synthetic network-flow data
- No direct packet capture
- No production network sensors
- Simplified statistical baselines
- Simplified alert correlation
- Local SQLite database
- Basic authentication architecture
- Limited threat-intelligence enrichment
- ML trained on synthetic data
- No production SIEM integration
- No distributed deployment

Machine-learning results should therefore not be interpreted as real-world enterprise detection performance.


---

# GitHub Repository

Repository:

```text
https://github.com/AkInnovates08/Network-Intrusion-Detection-System-Simulation
```

Recommended repository name:

```text
Network-Intrusion-Detection-System-Simulation
```

Recommended description:

```text
Defensive network intrusion detection simulation featuring synthetic traffic generation, signature-based and anomaly-based detection, hybrid risk scoring, alert correlation, SOC analytics, investigation workflows, and optional machine learning.
```

---



# Git Workflow

Initialize Git:

```bash
git init
```

Add files:

```bash
git add .
```

Create the first commit:

```bash
git commit -m "Initialize network IDS simulation"
```

Connect GitHub:

```bash
git remote add origin https://github.com/AkInnovates08/Network-Intrusion-Detection-System-Simulation.git
```

Rename branch:

```bash
git branch -M main
```

Push:

```bash
git push -u origin main
```

---

---

# Technical Skills Demonstrated

```text
Cybersecurity
Network Security
Intrusion Detection
SOC Operations
Network Traffic Analysis
Security Analytics
Python
FastAPI
React
SQLite
Pandas
NumPy
Scikit-learn
Machine Learning
Anomaly Detection
Signature Detection
Feature Engineering
Risk Scoring
Alert Management
Incident Investigation
REST APIs
Automated Testing
Git
GitHub
```



# Learning Outcomes

Through this project, the following concepts were practiced:

- Network security fundamentals
- Intrusion detection
- Network-flow analysis
- Security monitoring
- Feature engineering
- Rule-based detection
- Anomaly detection
- Machine learning for security analytics
- Risk scoring
- Alert generation
- Alert correlation
- SOC workflows
- Incident investigation
- Incident management
- REST API development
- Database design
- Dashboard development
- Automated testing
- Secure development practices

---

# Ethical Disclaimer

This project is designed exclusively for defensive cybersecurity education and authorized laboratory simulation.

All suspicious network behavior is represented using synthetic data records or authorized isolated environments.

The project does not provide functionality for:

- Public network scanning
- Unauthorized access
- Exploitation
- Credential theft
- DDoS attacks
- Network flooding
- Security bypass
- Attacking third-party systems

Users should only apply cybersecurity techniques to systems and networks they own or are explicitly authorized to test.

---

# Project Status

```text
Status: Completed
Project Type: Defensive Cybersecurity Simulation
Environment: Local / Synthetic
Detection: Hybrid IDS
Backend: FastAPI
Frontend: React + Vite
Dashboard: Streamlit
Database: SQLite
Machine Learning: Optional
Testing: Pytest
Dataset: Synthetic
```

---


---

# Conclusion

The Network Intrusion Detection System (IDS) Simulation demonstrates an end-to-end defensive security monitoring workflow using safe synthetic network-flow data.

The project combines network traffic simulation, feature engineering, signature-based detection, anomaly detection, machine learning, risk scoring, alert generation, database storage, SOC analytics, investigation filters, incident management, and analyst documentation into a single practical cybersecurity application.

It is intended as an educational and portfolio project demonstrating foundational skills relevant to SOC analysis, network security, cybersecurity engineering, threat detection, and security analytics.

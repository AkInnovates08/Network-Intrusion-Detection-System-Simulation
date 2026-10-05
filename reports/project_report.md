# Network Intrusion Detection System (IDS) Simulation — Project Report

## Abstract
This project implements a defensive Network Intrusion Detection System simulation using synthetic network-flow records. The system demonstrates feature extraction, signature/rule detection, statistical anomaly detection, optional machine learning, hybrid risk scoring, alert generation, correlation, persistence and SOC-style visualization without transmitting attack traffic.

## Introduction
Network intrusion detection helps security teams identify activity that deviates from expected behavior or matches known suspicious patterns. The project models this workflow in a self-contained local environment so a student can demonstrate practical cybersecurity engineering without real network access.

## Problem Statement
Students often learn IDS concepts theoretically but lack a safe environment in which to demonstrate detection engineering, alert triage and SOC workflows. The proposed system creates realistic-looking flow records and processes them through multiple defensive detection layers.

## Objectives
Generate synthetic data, engineer network features, implement rule and anomaly detection, optionally train ML models, score risk, generate alerts, correlate related alerts, persist events, expose APIs and provide a dashboard.

## Proposed System
The pipeline is: synthetic traffic -> collection -> feature extraction -> rules/anomaly/ML -> risk engine -> alert engine -> database -> SOC dashboard -> analyst investigation.

## Synthetic Dataset
The dataset contains fields for source/destination addresses, ports, protocol, packets, bytes, duration, connections, failures, SYN/RST counts, derived packet size, labels and scenario type. Documentation IP ranges are used.

## Detection
Rule detection is explainable and configurable. Anomaly detection calculates deviations across packet rate, byte rate, connection rate, failure ratio and destination-port diversity. Hybrid scoring reduces dependence on one detector.

## Machine Learning
Logistic Regression and Random Forest provide supervised classification, while Isolation Forest provides unsupervised anomaly detection. Evaluation metrics are generated from the dataset and should be reported from the actual run rather than fabricated.

## Risk Scoring
Risk is normalized to 0-100 and mapped to project-defined categories. These values are assumptions for an educational simulation and require calibration in real environments.

## SOC Workflow
Alerts can move from NEW to INVESTIGATING, RESOLVED or FALSE_POSITIVE. Analysts can add notes and use contextual investigation steps. Alert correlation reduces repetitive alert noise by grouping source/type/time-window combinations.

## Security and Privacy
The project avoids payload capture, uses synthetic data, keeps secrets in environment variables, and should add authentication, authorization, HTTPS, rate limiting and centralized audit logs before production use. IDS telemetry can itself be sensitive because it reveals hosts, services, communication patterns and security events.

## Testing
Automated tests cover validation, feature extraction, rule triggers, anomaly and risk scoring, and alert creation. API integration tests can be added after deployment hardening.

## Limitations
The system uses synthetic flows rather than real packet capture, simplified thresholds, SQLite and a local dashboard. It is not a production IDS and should not be represented as one.

## Future Scope
Authorized PCAP ingestion, Zeek/Suricata integration, SIEM forwarding, threat-intelligence enrichment, behavioral baselines, stronger anomaly models, cloud/container telemetry, centralized logging and model-drift monitoring.

## Conclusion
The project demonstrates a complete defensive detection lifecycle from synthetic telemetry through SOC investigation. Its strongest placement value is the combination of cybersecurity concepts, Python engineering, data analysis, ML evaluation and operational alert handling.

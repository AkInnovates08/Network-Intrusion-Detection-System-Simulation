# Architecture and Investigation Notes

## Components
1. Synthetic Traffic Generator: creates labeled flow records without sending traffic.
2. Flow Collector/API: receives one flow record and validates it.
3. Feature Extractor: derives rates, ratios and diversity indicators.
4. Rule Engine: applies explainable threshold-based detections.
5. Anomaly Detector: compares new features with a normal statistical baseline.
6. ML Layer: optional supervised classification and unsupervised Isolation Forest.
7. Risk Engine: combines signals into a bounded 0-100 score.
8. Alert Engine: converts meaningful detections into investigation records.
9. Correlation: groups repeated alerts by source, type and time window.
10. Database: stores flow metadata, alerts, rules and notes.
11. Dashboard: exposes SOC metrics, charts and recent alerts.

## Event vs Alert vs Incident
- Event: an individual observation.
- Alert: an observation that crossed a detection condition and requires attention.
- Incident: a collection of related alerts/events that requires investigation and documented response.

## Investigation checklist
- Confirm whether the source is known and expected.
- Compare the behavior with historical baseline.
- Review authentication and firewall logs where authorized.
- Review endpoint telemetry where authorized.
- Determine whether a maintenance, backup or business process explains the activity.
- Document evidence and analyst reasoning.
- Escalate according to organizational policy.

# Interview Preparation — 10 Questions and Answers

## 1. Explain your project.
I built a defensive Network Intrusion Detection System simulation that processes synthetic network-flow records. It extracts security features, applies configurable signature rules and statistical anomaly detection, optionally uses machine learning, combines the signals into a 0-100 risk score, generates alerts, stores them in SQLite and presents a SOC-style dashboard. I deliberately kept all suspicious behavior as data records so the project never attacks or scans a real system.

## 2. Why did you choose a network-based IDS?
Because it lets me demonstrate network security concepts without requiring physical infrastructure. Flow-level data is enough to show protocols, ports, rates, failures and behavioral baselines.

## 3. How does signature detection differ from anomaly detection?
Signature detection looks for known, explicit patterns such as a configured high connection rate. Anomaly detection compares behavior with a statistical baseline. Signatures are explainable and fast, while anomaly detection can identify unusual patterns but may create more false positives.

## 4. Why use a hybrid IDS?
Different detectors have different blind spots. Combining rules with anomaly scoring provides explainable detections plus behavioral coverage. The system can also include ML when the model is trained and evaluated.

## 5. How did you engineer features?
I derived bytes per second, packets per second, average packet size, failure ratio, SYN ratio, connection rate and destination-port diversity. These features describe traffic volume, connection behavior and protocol-level patterns without storing packet payloads.

## 6. How is risk score calculated?
Rule severity contributes a bounded rule score and is combined with anomaly score and, when enabled, ML probability using configurable weights. The final value is clamped to 0-100 and mapped to project-defined investigation categories.

## 7. Why are false positives important?
Legitimate events such as backups can look abnormal. Excessive false positives increase analyst workload and can cause alert fatigue. Better baselines, context, tuning and analyst feedback help reduce noise.

## 8. What is the role of machine learning?
ML is optional rather than the only detector. Logistic Regression and Random Forest provide supervised classification, while Isolation Forest is an unsupervised option. I evaluate the supervised models with accuracy, precision, recall, F1 and a confusion matrix.

## 9. What would you improve for production?
I would add authentication and authorization, HTTPS, centralized logging, a production database, real authorized telemetry, stronger baselines, SIEM integration, threat-intelligence enrichment, Zeek/Suricata inputs, alert deduplication and model-drift monitoring.

## 10. Why is this an IDS and not an IPS?
The project detects and alerts but does not automatically block traffic. That is intentional: automatic prevention could cause unintended disruption, while the student project is designed to demonstrate safe detection and SOC investigation.

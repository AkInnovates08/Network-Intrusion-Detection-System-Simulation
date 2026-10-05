from dataclasses import dataclass

@dataclass(frozen=True)
class IDSConfig:
    high_connection_rate: float = 12.0
    failed_connection_count: int = 5
    failure_ratio: float = 0.50
    unique_destination_ports: int = 8
    syn_ratio: float = 0.75
    high_bytes_per_second: float = 250_000.0
    unusual_ports: tuple = (23, 2323, 3389, 4444, 5900)
    anomaly_weight: float = 0.40
    rule_weight: float = 0.60
    ml_weight: float = 0.30
    no_ml_rule_weight: float = 0.60
    no_ml_anomaly_weight: float = 0.40

SEVERITY_ORDER = {"INFO": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}

import json
from pathlib import Path

def load_metrics(path="models/metrics.json"):
    p=Path(path)
    return json.loads(p.read_text()) if p.exists() else {}

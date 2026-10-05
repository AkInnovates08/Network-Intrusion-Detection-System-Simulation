import numpy as np

ANOMALY_FEATURES=["packets_per_second","bytes_per_second","connection_rate","failure_ratio","unique_destination_ports"]

def build_baseline(records):
    baseline={}
    for f in ANOMALY_FEATURES:
        vals=np.array([float(r.get(f,0)) for r in records], dtype=float)
        baseline[f]={"mean":float(vals.mean()) if len(vals) else 0.0,"std":float(vals.std(ddof=0)) if len(vals) else 0.0,"q1":float(np.percentile(vals,25)) if len(vals) else 0.0,"q3":float(np.percentile(vals,75)) if len(vals) else 0.0}
    return baseline

def calculate_anomaly_score(features, baseline):
    deviations=[]
    for f in ANOMALY_FEATURES:
        b=baseline.get(f,{"mean":0,"std":0}); std=b["std"]
        z=abs((float(features.get(f,0))-b["mean"])/std) if std > 1e-9 else 0.0
        deviations.append(min(z, 6.0)/6.0)
    return round(float(np.mean(deviations)*100),2)

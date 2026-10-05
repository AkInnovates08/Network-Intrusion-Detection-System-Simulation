from datetime import datetime, timezone
import uuid

def generate_alert(flow, rule_matches, risk_score, anomaly_score, ml_score=None):
    if not rule_matches and risk_score <= 20: return None
    top=max(rule_matches, key=lambda x:{"INFO":0,"LOW":1,"MEDIUM":2,"HIGH":3,"CRITICAL":4}.get(x["severity"],0)) if rule_matches else {"rule_id":"ANOM-001","name":"Behavioral Anomaly","severity":"MEDIUM","description":"Flow deviated from the statistical baseline."}
    return {"alert_id":"ALT-"+uuid.uuid4().hex[:8].upper(),"timestamp":datetime.now(timezone.utc).isoformat(),"source_ip":flow["source_ip"],"destination_ip":flow["destination_ip"],"protocol":flow["protocol"],"source_port":flow["source_port"],"destination_port":flow["destination_port"],"rule_id":top["rule_id"],"alert_type":top["name"],"severity":top["severity"],"risk_score":risk_score,"anomaly_score":anomaly_score,"ml_score":ml_score,"description":"; ".join(x["description"] for x in rule_matches) or top["description"],"status":"NEW"}

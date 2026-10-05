def calculate_risk_score(rule_matches, anomaly_score, ml_probability=None, weights=None):
    rule_score=min(100, sum({"INFO":10,"LOW":25,"MEDIUM":45,"HIGH":70,"CRITICAL":95}.get(m["severity"],20) for m in rule_matches))
    if ml_probability is None:
        w=weights or {"rule":.60,"anomaly":.40}; score=rule_score*w["rule"]+anomaly_score*w["anomaly"]
    else:
        w=weights or {"rule":.40,"anomaly":.30,"ml":.30}; score=rule_score*w["rule"]+anomaly_score*w["anomaly"]+float(ml_probability)*100*w["ml"]
    return round(max(0,min(100,score)),2)

def classify_risk(score):
    if score<=20:return "NORMAL"
    if score<=40:return "LOW RISK"
    if score<=60:return "SUSPICIOUS"
    if score<=80:return "HIGH RISK"
    return "CRITICAL INVESTIGATION"

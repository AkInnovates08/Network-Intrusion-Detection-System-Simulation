from .config import IDSConfig

def analyze_flow(features: dict, flow: dict, config: IDSConfig | None = None):
    c=config or IDSConfig(); matches=[]
    def add(rid,name,sev,desc): matches.append({"rule_id":rid,"name":name,"severity":sev,"description":desc})
    if features["connection_rate"] > c.high_connection_rate: add("IDS-001","High Connection Rate","HIGH","Connection rate exceeded configured baseline.")
    if features["failed_connection_count"] >= c.failed_connection_count or features["failure_ratio"] >= c.failure_ratio: add("IDS-002","Repeated Failed Connections","HIGH","Repeated connection failures exceeded configured baseline.")
    if features["unique_destination_ports"] >= c.unique_destination_ports: add("IDS-003","Destination Port Diversity","MEDIUM","One source was associated with unusually diverse destination ports.")
    if features["syn_ratio"] >= c.syn_ratio and features["connection_count"] >= 5: add("IDS-004","SYN-Heavy Behavior","MEDIUM","SYN activity was unusually high relative to connections.")
    if int(flow.get("destination_port",0)) in c.unusual_ports: add("IDS-005","Unusual Service Port","LOW","Destination port is outside the common service baseline for this simulation.")
    if features["bytes_per_second"] >= c.high_bytes_per_second: add("IDS-006","High Traffic Volume","HIGH","Byte rate exceeded the configured traffic baseline.")
    return matches

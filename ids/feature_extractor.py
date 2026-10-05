import ipaddress
from typing import Any

REQUIRED = ["packet_count","byte_count","duration_seconds","connection_count","failed_connection_count","syn_count","rst_count","source_port","destination_port","protocol","source_ip","destination_ip"]
PROTOCOLS = {"TCP", "UDP", "ICMP"}

def _num(v, default=0.0):
    try: return float(v)
    except (TypeError, ValueError): return default

def validate_flow(flow: dict[str, Any]) -> list[str]:
    errors=[]
    for k in REQUIRED:
        if k not in flow or flow[k] is None: errors.append(f"missing:{k}")
    for k in ("source_ip","destination_ip"):
        try: ipaddress.ip_address(str(flow.get(k)))
        except ValueError: errors.append(f"invalid:{k}")
    for k in ("source_port","destination_port"):
        v=flow.get(k)
        if not isinstance(v, int) or not 0 <= v <= 65535: errors.append(f"invalid:{k}")
    if str(flow.get("protocol", "")).upper() not in PROTOCOLS: errors.append("invalid:protocol")
    if _num(flow.get("duration_seconds")) < 0: errors.append("invalid:duration_seconds")
    for k in ("packet_count","byte_count","connection_count","failed_connection_count","syn_count","rst_count"):
        if _num(flow.get(k), -1) < 0: errors.append(f"invalid:{k}")
    return errors

def extract_network_features(flow: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, float]:
    duration=max(_num(flow.get("duration_seconds")), 1e-6)
    packets=_num(flow.get("packet_count")); bytes_= _num(flow.get("byte_count")); conns=_num(flow.get("connection_count")); failed=_num(flow.get("failed_connection_count")); syn=_num(flow.get("syn_count")); rst=_num(flow.get("rst_count"))
    avg=bytes_/packets if packets else 0.0
    ports=float((context or {}).get("unique_destination_ports", 1))
    ips=float((context or {}).get("unique_destination_ips", 1))
    return {"packet_count":packets,"byte_count":bytes_,"duration":duration,"bytes_per_second":bytes_/duration,"packets_per_second":packets/duration,"average_packet_size":avg,"connection_count":conns,"failed_connection_count":failed,"failure_ratio":failed/max(conns,1.0),"syn_count":syn,"rst_count":rst,"syn_ratio":syn/max(conns,1.0),"unique_destination_ports":ports,"unique_destination_ips":ips,"connection_rate":conns/duration}

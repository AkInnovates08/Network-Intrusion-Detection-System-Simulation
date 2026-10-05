from collections import defaultdict
from datetime import datetime

def correlate_alerts(alerts, window_seconds=60):
    groups=defaultdict(list)
    for a in alerts:
        try: ts=datetime.fromisoformat(a["timestamp"].replace("Z","+00:00"))
        except Exception: continue
        groups[(a["source_ip"],a["alert_type"])].append((ts,a))
    out=[]
    for key,items in groups.items():
        items.sort(); current=[items[0][1]]; start=items[0][0]
        for ts,a in items[1:]:
            if (ts-start).total_seconds()<=window_seconds: current.append(a)
            else: out.append({"source_ip":key[0],"alert_type":key[1],"count":len(current),"alerts":current}); current=[a]; start=ts
        out.append({"source_ip":key[0],"alert_type":key[1],"count":len(current),"alerts":current})
    return out

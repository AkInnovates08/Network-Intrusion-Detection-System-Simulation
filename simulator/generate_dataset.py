import argparse, csv, random, ipaddress
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCENARIOS={
"NORMAL_WEB":("NORMAL",443,"TCP"),"NORMAL_DNS":("NORMAL",53,"UDP"),"NORMAL_SSH":("NORMAL",22,"TCP"),"NORMAL_EMAIL":("NORMAL",587,"TCP"),"NORMAL_DATABASE":("NORMAL",5432,"TCP"),
"HIGH_CONNECTION_RATE":("SUSPICIOUS",443,"TCP"),"REPEATED_FAILED_CONNECTIONS":("SUSPICIOUS",22,"TCP"),"MULTI_PORT_PROBING_PATTERN":("SUSPICIOUS",80,"TCP"),"SYN_HEAVY_PATTERN":("SUSPICIOUS",443,"TCP"),"UNUSUAL_PORT_ACTIVITY":("SUSPICIOUS",4444,"TCP"),"HIGH_TRAFFIC_VOLUME":("SUSPICIOUS",443,"TCP")}

def ip_for(i, base): return str(ipaddress.ip_network(base)[i % 254 + 1])
def make_record(i, scenario, start):
    label,dport,proto=SCENARIOS[scenario]; src=ip_for(i,"192.0.2.0/24"); dst=ip_for(i*3+7,"198.51.100.0/24"); ts=start+timedelta(seconds=i*2)
    if scenario.startswith("NORMAL"):
        packets=random.randint(8,80); duration=random.uniform(.5,8); conns=random.randint(1,4); failed=random.choice([0,0,0,1]); syn=random.randint(0,max(1,conns)); rst=random.randint(0,1); ports=1
        if scenario=="NORMAL_DNS": packets=random.randint(2,15); duration=random.uniform(.05,1); conns=1; failed=0; syn=0
        if scenario=="NORMAL_DATABASE": packets=random.randint(30,120); duration=random.uniform(1,10); conns=random.randint(1,3)
    else:
        if scenario=="HIGH_CONNECTION_RATE": packets=250; duration=5; conns=random.randint(80,150); failed=random.randint(0,8); syn=conns//2; rst=random.randint(0,10); ports=1
        elif scenario=="REPEATED_FAILED_CONNECTIONS": packets=30; duration=12; conns=18; failed=random.randint(10,18); syn=16; rst=8; ports=1
        elif scenario=="MULTI_PORT_PROBING_PATTERN": packets=120; duration=15; conns=25; failed=8; syn=24; rst=10; ports=random.randint(10,25)
        elif scenario=="SYN_HEAVY_PATTERN": packets=150; duration=10; conns=30; failed=3; syn=29; rst=12; ports=3
        elif scenario=="UNUSUAL_PORT_ACTIVITY": packets=40; duration=3; conns=5; failed=1; syn=4; rst=1; ports=1
        else: packets=20000; duration=8; conns=12; failed=0; syn=8; rst=1; ports=1
    bytes_=int(packets*random.uniform(60,500))
    if scenario=="HIGH_TRAFFIC_VOLUME": bytes_=random.randint(3_000_000,8_000_000)
    return {"flow_id":f"FLOW-{i:06d}","timestamp":ts.isoformat(),"source_ip":src,"destination_ip":dst,"source_port":random.randint(1024,65535),"destination_port":dport,"protocol":proto,"packet_count":packets,"byte_count":bytes_,"duration_seconds":round(duration,3),"connection_count":conns,"failed_connection_count":failed,"syn_count":syn,"rst_count":rst,"average_packet_size":round(bytes_/packets,2),"label":label,"scenario_type":scenario,"unique_destination_ports":ports,"unique_destination_ips":1}

def generate(n=5000, out="data/network_traffic.csv", seed=42):
    random.seed(seed); Path(out).parent.mkdir(parents=True,exist_ok=True); start=datetime.now(timezone.utc)-timedelta(days=1)
    scenarios=list(SCENARIOS); rows=[]
    for i in range(n): rows.append(make_record(i, random.choices(scenarios,weights=[18,10,6,5,5,8,8,8,8,6,8],k=1)[0],start))
    fields=list(rows[0].keys())
    with open(out,"w",newline="",encoding="utf-8") as f: w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"Generated {n} synthetic flow records -> {out}")

if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--rows",type=int,default=5000); p.add_argument("--output",default="data/network_traffic.csv"); p.add_argument("--seed",type=int,default=42); a=p.parse_args(); generate(a.rows,a.output,a.seed)

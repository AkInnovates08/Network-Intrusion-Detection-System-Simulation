import csv
from backend.app import create_flow
from backend.db import init_db
from pathlib import Path
from types import SimpleNamespace

def seed(path="data/network_traffic.csv",limit=1000):
 init_db(); import pandas as pd
 df=pd.read_csv(path).head(limit)
 for _,r in df.iterrows():
  d=r.to_dict(); d["source_port"]=int(d["source_port"]); d["destination_port"]=int(d["destination_port"]); d["packet_count"]=int(d["packet_count"]); d["byte_count"]=int(d["byte_count"]); d["connection_count"]=int(d["connection_count"]); d["failed_connection_count"]=int(d["failed_connection_count"]); d["syn_count"]=int(d["syn_count"]); d["rst_count"]=int(d["rst_count"]); d["unique_destination_ports"]=int(d.get("unique_destination_ports",1)); d["unique_destination_ips"]=int(d.get("unique_destination_ips",1)); d["duration_seconds"]=float(d["duration_seconds"]); d.pop("average_packet_size",None); d.pop("label",None); d.pop("scenario_type",None); create_flow(SimpleNamespace(model_dump=lambda:d))
 print(f"Seeded {len(df)} flows")
if __name__=="__main__": seed()

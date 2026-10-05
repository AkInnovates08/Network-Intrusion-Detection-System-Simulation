import os, sqlite3, json
from pathlib import Path
DB_PATH=os.getenv("IDS_DB_PATH","data/ids.db")

def connect(): Path(DB_PATH).parent.mkdir(parents=True,exist_ok=True); c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row; return c

def init_db():
 c=connect(); c.executescript('''CREATE TABLE IF NOT EXISTS network_flows(flow_id TEXT PRIMARY KEY,timestamp TEXT,source_ip TEXT,destination_ip TEXT,source_port INTEGER,destination_port INTEGER,protocol TEXT,packet_count INTEGER,byte_count INTEGER,duration REAL,risk_score REAL,classification TEXT,raw_json TEXT); CREATE TABLE IF NOT EXISTS alerts(alert_id TEXT PRIMARY KEY,flow_id TEXT,rule_id TEXT,severity TEXT,description TEXT,risk_score REAL,status TEXT,created_at TEXT,alert_type TEXT,source_ip TEXT,destination_ip TEXT,protocol TEXT,source_port INTEGER,destination_port INTEGER,anomaly_score REAL,ml_score REAL); CREATE TABLE IF NOT EXISTS rules(rule_id TEXT PRIMARY KEY,rule_name TEXT,description TEXT,severity TEXT,threshold REAL,enabled INTEGER); CREATE TABLE IF NOT EXISTS incident_notes(note_id INTEGER PRIMARY KEY AUTOINCREMENT,alert_id TEXT,note TEXT,created_at TEXT); CREATE INDEX IF NOT EXISTS idx_alerts_created ON alerts(created_at); CREATE INDEX IF NOT EXISTS idx_alerts_source ON alerts(source_ip);'''); c.commit(); c.close()

def insert_flow(f):
 c=connect(); c.execute("INSERT OR REPLACE INTO network_flows VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",(f['flow_id'],f['timestamp'],f['source_ip'],f['destination_ip'],f['source_port'],f['destination_port'],f['protocol'],f['packet_count'],f['byte_count'],f['duration_seconds'],f.get('risk_score',0),f.get('classification','NORMAL'),json.dumps(f))); c.commit(); c.close()
def insert_alert(a,flow_id):
 c=connect(); c.execute("INSERT OR REPLACE INTO alerts VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(a['alert_id'],flow_id,a['rule_id'],a['severity'],a['description'],a['risk_score'],a['status'],a['timestamp'],a['alert_type'],a['source_ip'],a['destination_ip'],a['protocol'],a['source_port'],a['destination_port'],a.get('anomaly_score',0),a.get('ml_score'))); c.commit(); c.close()
def rows(q,args=()): c=connect(); r=[dict(x) for x in c.execute(q,args).fetchall()]; c.close(); return r

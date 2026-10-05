import sys
sys.path.insert(0,'.')
from ids.feature_extractor import extract_network_features,validate_flow
from ids.rule_engine import analyze_flow
from ids.anomaly_detector import build_baseline,calculate_anomaly_score
from ids.risk_engine import calculate_risk_score,classify_risk
from ids.alert_engine import generate_alert

def flow(**kw):
 d={'flow_id':'T','timestamp':'2026-01-01T00:00:00Z','source_ip':'192.0.2.10','destination_ip':'198.51.100.10','source_port':50000,'destination_port':443,'protocol':'TCP','packet_count':20,'byte_count':5000,'duration_seconds':2,'connection_count':2,'failed_connection_count':0,'syn_count':1,'rst_count':0,'unique_destination_ports':1,'unique_destination_ips':1};d.update(kw);return d

def test_valid_flow(): assert validate_flow(flow())==[]
def test_invalid_ip(): assert 'invalid:source_ip' in validate_flow(flow(source_ip='bad'))
def test_invalid_port(): assert 'invalid:source_port' in validate_flow(flow(source_port=70000))
def test_invalid_protocol(): assert 'invalid:protocol' in validate_flow(flow(protocol='GRE'))
def test_zero_duration_handled(): assert extract_network_features(flow(duration_seconds=0))['bytes_per_second']==5000000000.0
def test_high_connection_rule():
 f=flow(connection_count=100,duration_seconds=2); ft=extract_network_features(f); assert any(x['rule_id']=='IDS-001' for x in analyze_flow(ft,f))
def test_failed_rule():
 f=flow(connection_count=10,failed_connection_count=8); ft=extract_network_features(f); assert any(x['rule_id']=='IDS-002' for x in analyze_flow(ft,f))
def test_port_diversity_rule():
 f=flow(unique_destination_ports=12); ft=extract_network_features(f,{'unique_destination_ports':12,'unique_destination_ips':1}); assert any(x['rule_id']=='IDS-003' for x in analyze_flow(ft,f))
def test_syn_rule():
 f=flow(connection_count=20,syn_count=19); ft=extract_network_features(f); assert any(x['rule_id']=='IDS-004' for x in analyze_flow(ft,f))
def test_unusual_port_rule():
 f=flow(destination_port=4444); ft=extract_network_features(f); assert any(x['rule_id']=='IDS-005' for x in analyze_flow(ft,f))
def test_volume_rule():
 f=flow(byte_count=1000000,duration_seconds=2); ft=extract_network_features(f); assert any(x['rule_id']=='IDS-006' for x in analyze_flow(ft,f))
def test_baseline_score_range():
 f=extract_network_features(flow()); b=build_baseline([f]*30); assert 0<=calculate_anomaly_score(f,b)<=100
def test_risk_range(): assert 0<=calculate_risk_score([],50)<=100
def test_classification(): assert classify_risk(10)=='NORMAL'; assert classify_risk(90)=='CRITICAL INVESTIGATION'
def test_alert_creation():
 f=flow(connection_count=100,duration_seconds=2); ft=extract_network_features(f); rules=analyze_flow(ft,f); a=generate_alert(f,rules,80,40); assert a and a['severity']=='HIGH'
def test_normal_no_alert(): assert generate_alert(flow(),[],10,0) is None
def test_feature_keys():
 keys=extract_network_features(flow()).keys(); assert {'failure_ratio','syn_ratio','connection_rate'}.issubset(keys)
def test_missing_field(): assert 'missing:packet_count' in validate_flow({k:v for k,v in flow().items() if k!='packet_count'})
def test_negative_packets(): assert 'invalid:packet_count' in validate_flow(flow(packet_count=-1))
def test_negative_duration(): assert 'invalid:duration_seconds' in validate_flow(flow(duration_seconds=-1))
def test_destination_ip(): assert 'invalid:destination_ip' in validate_flow(flow(destination_ip='x'))
def test_port_boundary(): assert validate_flow(flow(source_port=0,destination_port=65535))==[]
# Additional coverage
for i in range(10):
    exec(f'def test_case_{i}():\n    assert 0 <= calculate_risk_score([], {i*10}) <= 100\n')

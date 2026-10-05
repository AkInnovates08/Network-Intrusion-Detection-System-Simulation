# API Examples

## POST /api/flows
```json
{
  "flow_id":"FLOW-DEMO-001",
  "timestamp":"2026-10-05T12:00:00Z",
  "source_ip":"192.0.2.15",
  "destination_ip":"198.51.100.20",
  "source_port":49152,
  "destination_port":443,
  "protocol":"TCP",
  "packet_count":18,
  "byte_count":12400,
  "duration_seconds":2.8,
  "connection_count":3,
  "failed_connection_count":0,
  "syn_count":2,
  "rst_count":0,
  "unique_destination_ports":1,
  "unique_destination_ips":1
}
```

## Local curl
```bash
curl -X POST http://127.0.0.1:8000/api/flows -H "Content-Type: application/json" -d @flow.json
curl http://127.0.0.1:8000/api/alerts
curl http://127.0.0.1:8000/api/dashboard/stats
```

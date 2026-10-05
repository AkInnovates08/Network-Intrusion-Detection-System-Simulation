# Safe Detection Scenario Matrix

| Scenario | Key input pattern | Expected detection | Expected class |
|---|---|---|---|
| Normal HTTPS | port 443, low rate, no failures | none | NORMAL |
| Normal DNS | UDP/53, short flows | none | NORMAL |
| Repeated Failed Connections | high failed count/ratio | IDS-002 | SUSPICIOUS/HIGH RISK |
| High Connection Rate | high connections per second | IDS-001 | SUSPICIOUS/HIGH RISK |
| Multi-Port Pattern | high destination-port diversity | IDS-003 | SUSPICIOUS |
| SYN-Heavy Pattern | high SYN ratio | IDS-004 | SUSPICIOUS |
| High Traffic Volume | high bytes/second | IDS-006 | SUSPICIOUS/HIGH RISK |
| Unusual Service Port | destination port 4444/other configured port | IDS-005 | SUSPICIOUS |

All rows represent data only. No packets are generated or transmitted.

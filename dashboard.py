import os, requests, pandas as pd, streamlit as st
import plotly.express as px
API=os.getenv("IDS_API_URL","http://127.0.0.1:8000")
st.set_page_config(page_title="Network IDS SOC",page_icon="🛡️",layout="wide")
st.title("Network Intrusion Detection System")
st.caption("Defensive synthetic network-flow simulation and SOC investigation dashboard")

def get(path,params=None):
 try: r=requests.get(API+path,params=params,timeout=3); r.raise_for_status(); return r.json()
 except Exception as e: st.error(f"API unavailable: {e}"); return []
st.sidebar.header("Investigation Filters")
status=st.sidebar.selectbox("Status",["All","NEW","INVESTIGATING","RESOLVED","FALSE_POSITIVE"]); severity=st.sidebar.selectbox("Severity",["All","INFO","LOW","MEDIUM","HIGH","CRITICAL"])
stats=get('/api/dashboard/stats'); cols=st.columns(6)
for c,k,label in zip(cols,['total','normal','suspicious','open_alerts','critical','avg_risk'],['Total Flows','Normal','Suspicious','Open Alerts','Critical','Avg Risk']): c.metric(label,round(stats.get(k) or 0,2))
traffic=pd.DataFrame(get('/api/dashboard/traffic'))
if not traffic.empty:
 c1,c2=st.columns(2); traffic['timestamp']=pd.to_datetime(traffic['timestamp']); c1.plotly_chart(px.line(traffic.sort_values('timestamp'),x='timestamp',y='risk_score',title='Risk Timeline'),use_container_width=True); c2.plotly_chart(px.histogram(traffic,x='protocol',title='Protocol Distribution'),use_container_width=True)
 c3,c4=st.columns(2); c3.plotly_chart(px.histogram(traffic,x='destination_port',title='Destination Port Distribution'),use_container_width=True); c4.plotly_chart(px.histogram(traffic,x='classification',title='Normal vs Suspicious'),use_container_width=True)
alerts=get('/api/alerts',{'limit':200,**({} if status=='All' else {'status':status}),**({} if severity=='All' else {'severity':severity})}); adf=pd.DataFrame(alerts)
st.subheader('Recent Alerts')
if not adf.empty:
 st.dataframe(adf[['alert_id','created_at','source_ip','destination_ip','protocol','alert_type','severity','risk_score','status']],use_container_width=True,hide_index=True)
 st.subheader('Alert Severity'); st.plotly_chart(px.histogram(adf,x='severity',title='Alerts by Severity'),use_container_width=True)
else: st.info('No alerts match the selected filters.')
if not adf.empty:
 st.subheader('Event Investigation')
 selected=st.selectbox('Select Alert',adf['alert_id'].tolist())
 detail=adf[adf.alert_id==selected].iloc[0].to_dict()
 left,right=st.columns(2)
 with left:
  st.json({k:detail.get(k) for k in ['alert_id','created_at','source_ip','destination_ip','protocol','source_port','destination_port','alert_type','severity','risk_score','anomaly_score','ml_score','status']})
 with right:
  st.markdown('**Defensive investigation checklist**')
  st.write('1. Review related logs and confirm whether the source is known.')
  st.write('2. Compare behavior with the historical baseline.')
  st.write('3. Check authentication and firewall records where authorized.')
  st.write('4. Review endpoint telemetry where authorized.')
  st.write('5. Determine whether the activity is expected and document evidence.')
  st.write('6. Escalate, resolve, or mark false positive according to policy.')
  st.info('Use the FastAPI status and notes endpoints to record the incident workflow.')


import argparse, json
from pathlib import Path
import joblib, pandas as pd
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
FEATURES=["packet_count","byte_count","duration_seconds","bytes_per_second","packets_per_second","connection_count","failed_connection_count","syn_count","rst_count","average_packet_size"]

def prepare(df):
    d=df.copy(); dur=d.duration_seconds.clip(lower=1e-6); d["bytes_per_second"]=d.byte_count/dur; d["packets_per_second"]=d.packet_count/dur; return d

def train(csv_path="data/network_traffic.csv", model_dir="models"):
    df=prepare(pd.read_csv(csv_path)); X=df[FEATURES].fillna(0); y=(df.label!="NORMAL").astype(int); Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=42,stratify=y)
    models={"logistic_regression":Pipeline([("scale",StandardScaler()),("model",LogisticRegression(max_iter=1000))]),"random_forest":RandomForestClassifier(n_estimators=200,random_state=42,class_weight="balanced")}
    Path(model_dir).mkdir(exist_ok=True); results={}
    for name,m in models.items():
        m.fit(Xtr,ytr); pred=m.predict(Xte); results[name]={"accuracy":accuracy_score(yte,pred),"precision":precision_score(yte,pred,zero_division=0),"recall":recall_score(yte,pred,zero_division=0),"f1":f1_score(yte,pred,zero_division=0),"confusion_matrix":confusion_matrix(yte,pred).tolist()}; joblib.dump(m,Path(model_dir)/f"{name}.joblib")
    iso=IsolationForest(contamination="auto",random_state=42); iso.fit(Xtr); joblib.dump(iso,Path(model_dir)/"isolation_forest.joblib")
    Path(model_dir,"metrics.json").write_text(json.dumps(results,indent=2)); print(json.dumps(results,indent=2)); return results
if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--csv",default="data/network_traffic.csv"); p.add_argument("--model-dir",default="models"); a=p.parse_args(); train(a.csv,a.model_dir)

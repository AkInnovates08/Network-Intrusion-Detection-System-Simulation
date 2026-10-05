from pathlib import Path
import joblib, pandas as pd
from .train_model import FEATURES,prepare

def predict(flow, model_path="models/random_forest.joblib"):
    df=prepare(pd.DataFrame([flow])); model=joblib.load(model_path); x=df[FEATURES].fillna(0); p=float(model.predict_proba(x)[0,1]) if hasattr(model,"predict_proba") else float(model.predict(x)[0]); return p

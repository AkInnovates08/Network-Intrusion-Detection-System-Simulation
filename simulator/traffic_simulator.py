import argparse,json,random,time
from .generate_dataset import make_record,SCENARIOS
from datetime import datetime,timezone

def run(mode="mixed",speed="slow"):
    delay=.25 if speed=="fast" else 1.5; i=1
    choices=["NORMAL_WEB","NORMAL_DNS","NORMAL_SSH","NORMAL_EMAIL"] if mode=="normal" else list(SCENARIOS)
    while True:
        scenario=random.choice(choices); event=make_record(i,scenario,datetime.now(timezone.utc)); event.pop("label",None); event.pop("scenario_type",None)
        print(json.dumps(event)); i+=1; time.sleep(delay)
if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--mode",choices=["normal","mixed"],default="mixed"); p.add_argument("--speed",choices=["slow","fast"],default="slow"); a=p.parse_args(); run(a.mode,a.speed)

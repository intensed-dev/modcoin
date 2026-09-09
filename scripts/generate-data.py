import json, math, random
from datetime import date, timedelta, datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
DAYS=365
end=date.today()
start=end-timedelta(days=DAYS-1)
rng=random.Random(260909)
price=10.0
rows=[]
for i in range(DAYS):
    d=start+timedelta(days=i)
    tod=math.sin(i/18.0)*0.018
    creator=(math.sin(i/7.0)+math.sin(i/29.0))*0.009
    noise=rng.uniform(-0.022,0.022)
    change=tod+creator+noise+0.0009
    op=price
    price=max(2.0, price*(1+change))
    close=price
    high=max(op,close)*(1+rng.uniform(.006,.035))
    low=min(op,close)*(1-rng.uniform(.006,.03))
    volume=int(1500000*(1+abs(change)*18+rng.random()*.8))
    rows.append({'date':d.isoformat(),'open':round(op,2),'high':round(high,2),'low':round(low,2),'close':round(close,2),'volume':volume})
    price=close

closes=[x['close'] for x in rows]
prev=rows[-2]['close']
current=rows[-1]
change_24h=(current['close']/prev-1)*100
current_data={'price':current['close'],'change_24h':round(change_24h,2),'market_cap':round(current['close']*100_000_000),'volume_24h':current['volume'],'ath':max(closes),'atl':min(closes),'updated_at':datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S'),'drivers':{'time':int((math.sin(datetime.now(timezone.utc).hour/24*math.tau)+1)*50),'creator':int((math.sin(end.toordinal()/7)+1)*50),'noise':int(rng.random()*55)}}
DATA.mkdir(exist_ok=True)
(DATA/'history.json').write_text(json.dumps(rows,indent=2)+'\n')
(DATA/'current.json').write_text(json.dumps(current_data,separators=(',',':'))+'\n')

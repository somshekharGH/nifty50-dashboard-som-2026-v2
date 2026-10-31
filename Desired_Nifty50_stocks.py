from flask import Flask, render_template_string
import yfinance as yf
app = Flask(__name__)

NIFTY50 = ["RELIANCE","TCS","INFY","HDFCBANK","ICICIBANK","SBIN","BHARTIARTL","ITC","LT","KOTAKBANK","AXISBANK","BAJFINANCE","MARUTI","ASIANPAINT","HCLTECH","WIPRO","SUNPHARMA","TITAN","ULTRACEMCO","NESTLEIND","POWERGRID","NTPC","ONGC","M&M","TATAMOTORS","JSWSTEEL","TATASTEEL","HINDALCO","COALINDIA","GRASIM","ADANIENT","ADANIPORTS","BAJAJFINSV","BAJAJ-AUTO","BRITANNIA","CIPLA","DIVISLAB","DRREDDY","EICHERMOT","HEROMOTOCO","HINDUNILVR","INDUSINDBK","SBILIFE","SHRIRAMFIN","TECHM","APOLLOHOSP","BPCL","LTIM","TRENT","BEL"]

def get_hist(sym):
    for t in [sym+".NS", sym.replace("&","%26")+".NS"]:
        try:
            h = yf.Ticker(t).history(period="1y")
            if not h.empty and len(h)>20: return h
        except: pass
    return yf.Ticker(sym+".NS").history(period="1y")

def calc_rsi(s,p=14):
    d=s.diff(); g=d.where(d>0,0).rolling(p).mean(); l=-d.where(d<0,0).rolling(p).mean()
    return 100-(100/(1+g/l))

@app.route("/")
def home():
    rows=[]
    for sym in NIFTY50:
        hist=get_hist(sym)
        if hist.empty: 
            rows.append({"s":sym,"cmp":0,"dr":0,"wr":0,"sig":"NO DATA","cl":"neutral","mp":0,"hi":0,"lo":0}); continue
        close=hist['Close']; cmp=round(close.iloc[-1],2)
        dr=round(calc_rsi(close).iloc[-1],1); wr=round(calc_rsi(close.resample('W').last()).iloc[-1],1)
        sig,cl="NEUTRAL","neutral"
        if dr>60 and wr>60: sig,cl="BULLISH","bullish"
        elif dr<40 and wr<40: sig,cl="BEARISH","bearish"
        mp=round(((close.iloc[-1]-close.iloc[-21])/close.iloc[-21]*100),1) if len(close)>21 else 0
        rows.append({"s":sym,"cmp":cmp,"dr":dr,"wr":wr,"sig":sig,"cl":cl,"mp":mp,"hi":round(hist['High'].max(),1),"lo":round(hist['Low'].min(),1)})
    rows.sort(key=lambda x: x['dr'], reverse=True)
    
    html_template = """
    <html><head>
    <style>body{font-family:Arial;background:#f0f2f5;padding:12px}.card{background:white;padding:14px;border-radius:12px;box-shadow:0 2px 6px #ccc;margin-bottom:12px}table{width:100%;border-collapse:collapse;font-size:13px}th,td{padding:10px;border-bottom:1px solid #ddd;text-align:center}th{background:#0a66ff;color:white;cursor:pointer}th:hover{background:#084ec0}.bullish{background:green;color:white;padding:4px 10px;border-radius:12px}.bearish{background:red;color:white;padding:4px 10px;border-radius:12px}.neutral{background:#ffcc00;padding:4px 10px;border-radius:12px}</style>
    <script>
    let sortDir = {};
    function sortTable(col){
        let table = document.getElementById("stockTable");
        let tbody = table.tBodies[0];
        let rows = Array.from(tbody.rows);
        let dir = sortDir[col] === 'asc' ? 'desc' : 'asc';
        sortDir[col] = dir;
        rows.sort((a,b)=>{
            let av = a.cells[col].innerText.trim();
            let bv = b.cells[col].innerText.trim();
            // Number wale columns: 1,2,3,5,6,7
            if([1,2,3,5,6,7].includes(col)){
                av = parseFloat(av.replace('₹','').replace('%','')) || -99999;
                bv = parseFloat(bv.replace('₹','').replace('%','')) || -99999;
                return dir==='asc' ? av-bv : bv-av;
            } else {
                // Text wale columns: 0 Stock, 4 Signal
                return dir==='asc' ? av.localeCompare(bv) : bv.localeCompare(av);
            }
        });
        rows.forEach(r=>tbody.appendChild(r));
    }
    </script>
    </head>
    <body>
    <div class="card"><h2>📊 Nifty50 Dashboard ({{count}}/50) - Header par click karo ↕️</h2></div>
    <div class="card" style="overflow:auto">
    <table id="stockTable">
    <thead><tr>
    <th onclick="sortTable(0)">Stock ↕️</th>
    <th onclick="sortTable(1)">CMP ↕️</th>
    <th onclick="sortTable(2)">Daily RSI ↕️</th>
    <th onclick="sortTable(3)">Weekly RSI ↕️</th>
    <th onclick="sortTable(4)">Signal ↕️</th>
    <th onclick="sortTable(5)">Monthly% ↕️</th>
    <th onclick="sortTable(6)">52W High ↕️</th>
    <th onclick="sortTable(7)">52W Low ↕️</th>
    </tr></thead>
    <tbody>
    {% for r in rows %}
    <tr><td><b>{{r.s}}</b></td><td>₹{{r.cmp}}</td><td>{{r.dr}}</td><td>{{r.wr}}</td><td><span class="{{r.cl}}">{{r.sig}}</span></td><td>{{r.mp}}%</td><td>{{r.hi}}</td><td>{{r.lo}}</td></tr>
    {% endfor %}
    </tbody>
    </table>
    </div>
    </body></html>
    """
    return render_template_string(html_template, rows=rows, count=len(rows))

if __name__=="__main__":
    app.run(port=5001, debug=False)
import requests
import time
import pandas as pd

def fetch_nse_option_chain(symbol="NIFTY"):
    # 1. బ్రౌజర్ లాగా నటించడానికి Headers సెట్ చేయడం
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br"
    }

    # 2. ఒకే సెషన్ (Session) ని మెయింటైన్ చేయడం
    session = requests.Session()
    session.headers.update(headers)

    try:
        # 3. ముందుగా NSE హోమ్ పేజీకి వెళ్లి Cookies సేవ్ చేసుకోవడం (బైపాస్ ట్రిక్)
        session.get("https://www.nseindia.com", timeout=10)
        time.sleep(1) # సర్వర్ మీద లోడ్ పడకుండా 1 సెకను గ్యాప్
        
        # 4. ఆప్షన్ చైన్ API ని హిట్ చేయడం
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
        response = session.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            records = data.get('records', {}).get('data', [])
            
            # 5. వచ్చిన డేటాని టేబుల్ (DataFrame) ఫార్మాట్ లోకి మార్చడం
            chain_data = []
            for item in records:
                strike = item.get('strikePrice')
                ce = item.get('CE', {})
                pe = item.get('PE', {})
                
                chain_data.append({
                    "CE OI": ce.get('openInterest', 0),
                    "CE Volume": ce.get('totalTradedVolume', 0),
                    "CE LTP": ce.get('lastPrice', 0),
                    "Strike Price": strike,
                    "PE LTP": pe.get('lastPrice', 0),
                    "PE Volume": pe.get('totalTradedVolume', 0),
                    "PE OI": pe.get('openInterest', 0)
                })
                
            df = pd.DataFrame(chain_data)
            return df
        else:
            print(f"❌ Error: {response.status_code} - సర్వర్ బ్లాక్ చేసింది లేదా డేటా రాలేదు.")
            return None
            
    except Exception as e:
        print(f"❌ కనెక్షన్ ఫెయిల్ అయ్యింది: {e}")
        return None

# లైవ్ మార్కెట్ లో ప్రతి 5 సెకన్లకు ఒకసారి డేటా అప్డేట్ అవ్వడానికి Loop
if __name__ == "__main__":
    symbol_to_track = "NIFTY"  # మీరు BANKNIFTY కావాలంటే ఇక్కడ మార్చుకోవచ్చు
    
    print(f"🚀 {symbol_to_track} ఆప్షన్ చైన్ స్కానర్ స్టార్ట్ అయ్యింది. ఆపడానికి 'Ctrl + C' నొక్కండి.")
    print("-" * 70)
    
    while True:
        try:
            print(f"\n⏳ డేటా తీసుకువస్తోంది... సమయం: {time.strftime('%H:%M:%S')}")
            df = fetch_nse_option_chain(symbol_to_track)
            
            if df is not None:
                # వందల కొద్దీ స్ట్రైక్స్ వస్తాయి కాబట్టి, సపోర్ట్ కోసం మధ్యలో ఉన్న కొన్ని స్ట్రైక్స్ మాత్రమే ప్రింట్ చేద్దాం
                # నచ్చితే మొత్తం చూడటానికి print(df) వాడొచ్చు
                print(df.dropna().head(10).to_string(index=False))
                
                # డేటాని ఎక్సెల్ ఫైల్ గా సేవ్ చేయాలనుకుంటే కింద ఉన్న లైన్ వాడొచ్చు (కానీ లైవ్ లో వద్దు)
                # df.to_excel("Live_Options_Data.xlsx", index=False)
                
            time.sleep(5) # ⚠️ ప్రతి రిక్వెస్ట్ కి మధ్యలో 5 సెకన్ల గ్యాప్ (బ్లాక్ అవ్వకుండా ఉండటానికి)
            
        except KeyboardInterrupt:
            print("\n🛑 స్కానర్ ఆపబడింది.")
            break

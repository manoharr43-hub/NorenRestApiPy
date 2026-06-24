import os
from dotenv import load_dotenv
from fyers_apiv3 import fyersModel

# 1. .env ఫైల్ నుండి సీక్రెట్ కీస్ ని సురక్షితంగా లోడ్ చేయడం
load_dotenv()
client_id = os.getenv("FYERS_CLIENT_ID")
secret_key = os.getenv("FYERS_SECRET_KEY")
redirect_uri = "https://127.0.0.1" 
response_type = "code"  
grant_type = "authorization_code"  

def generate_fyers_token():
    # 2. సెషన్ క్రియేట్ చేయడం
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type=response_type,
        grant_type=grant_type
    )

    # 3. లాగిన్ లింక్ జనరేట్ చేయడం
    auth_link = session.generate_authcode()
    print("\n" + "="*70)
    print("STEP 1: కింది లింక్‌ని కాపీ చేసి గూగుల్ క్రోమ్ బ్రౌజర్‌లో ఓపెన్ చేయండి:")
    print("="*70)
    print(auth_link)
    print("="*70 + "\n")

    # 4. యూజర్ లాగిన్ అయ్యే వరకు వెయిట్ చేసి, Auth Code అడగడం
    print("STEP 2: బ్రౌజర్ లో లాగిన్ అయ్యాక, పైనున్న URL ఇలా మారుతుంది:")
    print("https://127.0.0.1/?auth_code=XXXXXXXX&state=None")
    print("అందులో 'auth_code=' తర్వాత ఉన్న ఆ XXXXXXXX కోడ్ ని మాత్రమే కాపీ చేయండి.\n")
    
    auth_code = input("👉 ఇక్కడ మీ Auth Code ని పేస్ట్ చేసి Enter నొక్కండి: ")

    # 5. Access Token జనరేట్ చేయడం
    session.set_token(auth_code)
    response = session.generate_token()

    # 6. టోకెన్ వచ్చిందో లేదో చెక్ చేసి, దాన్ని సేవ్ చేయడం
    if response.get("s") == "ok":
        access_token = response["access_token"]
        print("\n✅ సక్సెస్! మీ Access Token జనరేట్ అయ్యింది.")
        
        # భవిష్యత్తులో NSE AI PRO వాడుకోవడానికి టోకెన్ ని ఒక ఫైల్ లో సేవ్ చేయడం
        with open("access_token.txt", "w") as f:
            f.write(access_token)
            
        print("📁 టోకెన్ విజయవంతంగా 'access_token.txt' ఫైల్ లో సేవ్ చేయబడింది!")
        print("ఇక మీ డ్యాష్‌బోర్డ్ ద్వారా లైవ్ ట్రేడింగ్ డేటాని పొందవచ్చు.")
    else:
        print("\n❌ ఎర్రర్ వచ్చింది. దయచేసి వివరాలు చెక్ చేయండి:")
        print(response)

# ప్రోగ్రామ్ రన్ చేయడం
if __name__ == "__main__":
    generate_fyers_token()

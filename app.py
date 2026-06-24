import streamlit as st
from fyers_apiv3 import fyersModel
import os
from dotenv import load_dotenv

# లోకల్ లో టెస్ట్ చేసినప్పుడు .env ఫైల్ నుండి కీస్ తీసుకుంటుంది
load_dotenv()

# --- Configuration ---
# Streamlit Secrets లేదా Environment variables నుండి కీస్ తీసుకుంటుంది
client_id = os.getenv("FYERS_CLIENT_ID") or st.secrets.get("FYERS_CLIENT_ID")
secret_key = os.getenv("FYERS_SECRET_KEY") or st.secrets.get("FYERS_SECRET_KEY")

# ముఖ్యమైనది: మీ ఆన్‌లైన్ Streamlit లింక్ (ఇది Fyers డాష్‌బోర్డ్‌లో ఇచ్చిన లింక్‌తో కచ్చితంగా మ్యాచ్ అవ్వాలి)
redirect_uri = "https://manoharr43-hub-norenrestapipy-ap-hk1emv.streamlit.app/"

# --- UI Setup ---
st.set_page_config(page_title="My Fyers Algo", page_icon="📈")
st.title("📈 My Fyers Algo Trading App")

# కీస్ లేకపోతే ఎర్రర్ చూపించడానికి
if not client_id or not secret_key:
    st.error("⚠️ API Keys దొరకలేదు! దయచేసి Streamlit Secrets లేదా .env ఫైల్ చెక్ చేయండి.")
    st.stop()

# Fyers Session స్టార్ట్ చేయడం
session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type="code",
    grant_type="authorization_code"
)

# --- OAuth Flow (లాగిన్ ప్రాసెస్) ---
# URL లో 'auth_code' ఉందో లేదో చెక్ చేస్తుంది (లాగిన్ అయ్యాక ఇది వస్తుంది)
query_params = st.query_params

if "auth_code" in query_params:
    auth_code = query_params["auth_code"]
    st.success("ఆథరైజేషన్ కోడ్ వచ్చింది! లాగిన్ కనెక్ట్ అవుతోంది...")
    
    # Access Token జనరేట్ చేయడం
    session.set_token(auth_code)
    response = session.generate_token()
    
    if "access_token" in response:
        access_token = response["access_token"]
        st.success("✅ లాగిన్ సక్సెస్ (Login Successful)!")
        
        # Fyers Model ని టోకెన్ తో ఇనిషియలైజ్ చేయడం
        fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")
        
        # యూజర్ ప్రొఫైల్ డీటెయిల్స్ తీసుకోవడం
        profile = fyers.get_profile()
        if profile['s'] == 'ok':
            name = profile['data']['name']
            st.write(f"### స్వాగతం, {name} గారు! 🎉")
            st.write("మీ ప్రొఫైల్ వివరాలు:")
            st.json(profile['data']) # ప్రొఫైల్ డేటాని చూపిస్తుంది
        else:
            st.error("ప్రొఫైల్ వివరాలు తీసుకురావడంలో లోపం జరిగింది.")
            st.write(profile)
            
    else:
        st.error("❌ లాగిన్ ఫెయిల్ అయింది. Access Token రాలేదు.")
        st.write(response)

else:
    # యూజర్ ఇంకా లాగిన్ అవ్వకపోతే లింక్ చూపిస్తుంది
    auth_link = session.generate_authcode()
    st.markdown(f"### 🔐 [Fyers కి లాగిన్ అవ్వడానికి ఇక్కడ క్లిక్ చేయండి]({auth_link})")
    st.caption("ట్రేడింగ్ ఫీచర్స్ వాడటానికి పైన ఉన్న లింక్ ద్వారా లాగిన్ అవ్వండి.")

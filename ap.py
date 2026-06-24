import streamlit as st
import os
from fyers_apiv3 import fyersModel

# Streamlit పేజీ సెట్టింగ్స్
st.set_page_config(page_title="NSE AI PRO", layout="centered")
st.title("📈 NSE AI PRO - Fyers Login")

# Streamlit Secrets నుండి కీస్ తీసుకోవడం (లేదా మీ .env నుండి)
# మీరు లోకల్ గా రన్ చేస్తుంటే st.secrets బదులు os.getenv వాడండి
try:
    client_id = st.secrets["FYERS_CLIENT_ID"]
    secret_key = st.secrets["FYERS_SECRET_KEY"]
except:
    # లోకల్ సిస్టమ్ కోసం (ఒకవేళ secrets లేకపోతే)
    from dotenv import load_dotenv
    load_dotenv()
    client_id = os.getenv("FYERS_CLIENT_ID")
    secret_key = os.getenv("FYERS_SECRET_KEY")

redirect_uri = "https://127.0.0.1" 
response_type = "code"  
grant_type = "authorization_code"  

# సెషన్ క్రియేట్ చేయడం
session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type=response_type,
    grant_type=grant_type
)

# స్టెప్ 1: లాగిన్ లింక్ చూపించడం
auth_link = session.generate_authcode()
st.subheader("Step 1: కింది లింక్ ద్వారా లాగిన్ అవ్వండి")
st.markdown(f"**[👉 Fyers లాగిన్ కోసం ఇక్కడ క్లిక్ చేయండి]({auth_link})**")
st.info("లాగిన్ అయ్యాక, అడ్రస్ బార్‌లోని URL లో `auth_code=` తర్వాత ఉన్న కోడ్ ని మాత్రమే కాపీ చేయండి.")

st.divider()

# స్టెప్ 2: Auth Code ఎంటర్ చేయడానికి బాక్స్
st.subheader("Step 2: Auth Code ని ఇక్కడ పేస్ట్ చేయండి")
auth_code = st.text_input("మీ Auth Code ఇక్కడ ఇవ్వండి:", type="password")

# బటన్ నొక్కినప్పుడు టోకెన్ జనరేట్ చేయడం
if st.button("Generate Access Token"):
    if auth_code:
        session.set_token(auth_code)
        response = session.generate_token()

        if response.get("s") == "ok":
            st.success("✅ సక్సెస్! మీ Access Token జనరేట్ అయ్యింది. మీరు ఇప్పుడు ట్రేడింగ్ డేటా పొందవచ్చు.")
            
            # టోకెన్ ని వేరే ఫంక్షన్స్ కోసం సేవ్ చేసుకోవడం
            st.session_state['access_token'] = response["access_token"]
            
            # కావాలంటే టోకెన్ వివరాలు ప్రింట్ చేయొచ్చు (సెక్యూరిటీ కోసం డిస్ప్లే చేయకండి)
            st.write("ఇక మనం లైవ్ డేటా మరియు చార్ట్స్ వైపు వెళ్లొచ్చు!")
        else:
            st.error("❌ ఎర్రర్ వచ్చింది. దయచేసి సరైన కోడ్ ని ఇవ్వండి లేదా వివరాలు చెక్ చేయండి.")
            st.json(response)
    else:
        st.warning("ముందుగా పై బాక్స్ లో Auth Code ని ఎంటర్ చేయండి.")

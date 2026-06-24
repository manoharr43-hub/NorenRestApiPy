import streamlit as st
import urllib.parse as urlparse
from fyers_apiv3 import fyersModel

# 1. Streamlit Secrets నుండి సురక్షితంగా ఐడీలను తీసుకోవడం
try:
    client_id = st.secrets["FYERS_CLIENT_ID"]
    secret_key = st.secrets["FYERS_SECRET_KEY"]
except KeyError:
    st.error("కొత్త సీక్రెట్స్ ఇంకా అప్‌డేట్ కాలేదు. దయచేసి Streamlit సెట్టింగ్స్ చెక్ చేయండి.")
    st.stop()

redirect_uri = "https://127.0.0.1"
response_type = "code"
grant_type = "authorization_code"

# 2. ఫయర్స్ సెషన్ క్రియేట్ చేయడం
session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type=response_type,
    grant_type=grant_type
)

# ==========================================
# UI డిజైన్
# ==========================================

st.subheader("Step 1: కింది లింక్ ద్వారా ఫయర్స్ లో లాగిన్ అవ్వండి")
auth_link = session.generate_authcode()
st.markdown(f"[👉 **ఇక్కడ క్లిక్ చేసి Fyers లో లాగిన్ అవ్వండి**]({auth_link})")

st.markdown("---")

st.subheader("Step 2: రీడైరెక్ట్ అయిన మొత్తం URL ని ఇక్కడ పేస్ట్ చేయండి")
full_url = st.text_input("పైన అడ్రస్ బార్ లో ఉన్న మొత్తం లింక్ ని ఇక్కడ ఇవ్వండి:", type="password")

if st.button("Generate Access Token"):
    if full_url:
        try:
            parsed = urlparse.urlparse(full_url)
            auth_code = urlparse.parse_qs(parsed.query)['auth_code'][0]
            
            session.set_token(auth_code)
            response = session.generate_token()

            if response.get("s") == "ok":
                st.success("✅ సక్సెస్! మీ Access Token జనరేట్ అయ్యింది.")
                st.session_state['access_token'] = response["access_token"]
                st.write("ఇక మనం NSE AI PRO లో లైవ్ డేటా మరియు చార్ట్స్ వైపు వెళ్లొచ్చు!")
            else:
                st.error("❌ ఎర్రర్ వచ్చింది. దయచేసి మళ్ళీ లాగిన్ అయ్యి ట్రై చేయండి.")
                st.json(response)
                
        except Exception as e:
            st.error("❌ మీరు ఇచ్చిన లింక్ లో తప్పుంది. దయచేసి 'https://127.0.0.1/...' తో మొదలయ్యే మొత్తం URL ని కాపీ చేసి పేస్ట్ చేయండి.")
    else:
        st.warning("ముందుగా పై బాక్స్ లో లాగిన్ అయ్యాక వచ్చిన మొత్తం లింక్ ని ఎంటర్ చేయండి.")
# కోడ్ లో ఇక్కడ యాడ్ చేయండి:
st.write(f"DEBUG: వాడుతున్న Client ID: {client_id[:4]}****") 

import streamlit as st
import urllib.parse as urlparse
from fyers_apiv3 import fyersModel

# 1. మీ ఫయర్స్ యాప్ వివరాలు (మీ ఐడీలు ఇక్కడే ఇచ్చాను)
client_id = "1VFMW4AYYQ-200"
secret_key = "ztI67zCj3BfPDbhy"
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
# UI డిజైన్ (స్క్రీన్ మీద కనిపించేది)
# ==========================================

# Step 1: లాగిన్ లింక్ జనరేట్ చేయడం
st.subheader("Step 1: కింది లింక్ ద్వారా ఫయర్స్ లో లాగిన్ అవ్వండి")
auth_link = session.generate_authcode()
st.markdown(f"[👉 **ఇక్కడ క్లిక్ చేసి Fyers లో లాగిన్ అవ్వండి**]({auth_link})")

st.markdown("---")

# Step 2: కాపీ చేసిన లింక్ ని పేస్ట్ చేయడం
st.subheader("Step 2: రీడైరెక్ట్ అయిన మొత్తం URL ని ఇక్కడ పేస్ట్ చేయండి")
full_url = st.text_input("పైన అడ్రస్ బార్ లో ఉన్న మొత్తం లింక్ ని ఇక్కడ ఇవ్వండి:", type="password")

if st.button("Generate Access Token"):
    if full_url:
        try:
            # మీరు ఇచ్చిన మొత్తం లింక్ నుండి 'auth_code' ని సిస్టమ్ ఆటోమేటిక్ గా లాగుతుంది
            parsed = urlparse.urlparse(full_url)
            auth_code = urlparse.parse_qs(parsed.query)['auth_code'][0]
            
            # ఆ కోడ్ తో యాక్సెస్ టోకెన్ తెచ్చుకోవడం
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

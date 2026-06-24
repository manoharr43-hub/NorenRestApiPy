import streamlit as st
import os
import urllib.parse as urlparse # ఇది కొత్తగా యాడ్ చేసాం
from fyers_apiv3 import fyersModel

# --- మీ పాత సెట్టింగ్స్ మరియు Step 1 కోడ్ ఇక్కడ అలాగే ఉంచండి ---

# స్టెప్ 2: మొత్తం URL ఎంటర్ చేయడానికి బాక్స్
st.subheader("Step 2: రీడైరెక్ట్ అయిన మొత్తం URL ని ఇక్కడ పేస్ట్ చేయండి")
full_url = st.text_input("పైన అడ్రస్ బార్ లో ఉన్న మొత్తం లింక్ ని ఇక్కడ ఇవ్వండి:", type="password")

# బటన్ నొక్కినప్పుడు టోకెన్ జనరేట్ చేయడం
if st.button("Generate Access Token"):
    if full_url:
        try:
            # 1. మీరు ఇచ్చిన మొత్తం URL నుండి 'auth_code' ని ఆటోమేటిక్ గా వేరు చేయడం
            parsed = urlparse.urlparse(full_url)
            auth_code = urlparse.parse_qs(parsed.query)['auth_code'][0]
            
            # 2. ఆ కరెక్ట్ కోడ్ ని Fyers కి పంపడం
            session.set_token(auth_code)
            response = session.generate_token()

            if response.get("s") == "ok":
                st.success("✅ సక్సెస్! మీ Access Token జనరేట్ అయ్యింది. మీరు ఇప్పుడు ట్రేడింగ్ డేటా పొందవచ్చు.")
                st.session_state['access_token'] = response["access_token"]
                st.write("ఇక మనం లైవ్ డేటా మరియు చార్ట్స్ వైపు వెళ్లొచ్చు!")
            else:
                st.error("❌ ఎర్రర్ వచ్చింది. దయచేసి మళ్ళీ కొత్తగా లాగిన్ అయ్యి ట్రై చేయండి.")
                st.json(response)
                
        except Exception as e:
            st.error("❌ మీరు ఇచ్చిన లింక్ లో తప్పుంది. దయచేసి 'https://127.0.0.1/...' తో మొదలయ్యే మొత్తం URL ని కాపీ చేసి పేస్ట్ చేయండి.")
    else:
        st.warning("ముందుగా పై బాక్స్ లో లాగిన్ అయ్యాక వచ్చిన మొత్తం లింక్ ని ఎంటర్ చేయండి.")

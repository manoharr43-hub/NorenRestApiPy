import streamlit as st
import os
from dotenv import load_dotenv
from fyers_apiv3 import fyersModel

# పేజీ సెట్టింగ్స్
st.set_page_config(page_title="Fyers Algo Trading", layout="wide")

# 1. .env ఫైల్ నుండి కీస్ లోడ్ చేయడం
load_dotenv()
client_id = os.getenv("FYERS_CLIENT_ID")
secret_key = os.getenv("FYERS_SECRET_KEY")

# Fyers డాష్‌బోర్డ్‌లో మీరు ఇచ్చిన Redirect URL కచ్చితంగా ఇదే అయి ఉండాలి
redirect_uri = "http://localhost:8501/" 

st.title("📈 My Fyers Algo Trading App")

# API కీస్ ఉన్నాయో లేదో చెక్ చేయడం
if not client_id or not secret_key:
    st.error("⚠️ API Keys దొరకలేదు! దయచేసి .env ఫైల్‌ని సరిగ్గా సెట్ చేశారో లేదో చెక్ చేయండి.")
    st.stop()

# 2. Fyers సెషన్ సెటప్
session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type="code",
    grant_type="authorization_code"
)

# 3. ఆథరైజేషన్ (Authentication) విధానం
query_params = st.query_params

# సెషన్ లో యాక్సెస్ టోకెన్ లేకపోతే, లాగిన్ ప్రాసెస్ స్టార్ట్ చేయాలి
if "access_token" not in st.session_state:
    
    # URL లో 'auth_code' ఉందో లేదో చెక్ చేస్తుంది (లాగిన్ అయ్యాక వస్తుంది)
    if "auth_code" in query_params:
        auth_code = query_params["auth_code"]
        st.info("✅ Auth Code దొరికింది! Access Token జనరేట్ చేస్తున్నాం...")
        
        # టోకెన్ జనరేట్ చేయడం
        session.set_token(auth_code)
        response = session.generate_token()
        
        if response.get("s") == "ok":
            access_token = response["access_token"]
            
            # టోకెన్ ని సెషన్ లో సేవ్ చేయడం (పేజీ రీలోడ్ అయినా పోకుండా ఉండటానికి)
            st.session_state["access_token"] = access_token
            st.success("🎉 లాగిన్ సక్సెస్! యాక్సెస్ టోకెన్ జనరేట్ అయ్యింది.")
            
            # URL ని క్లీన్ చేసి పేజీని రీఫ్రెష్ చేయడం
            st.query_params.clear()
            st.rerun()
        else:
            st.error(f"❌ లాగిన్ ఫెయిల్ అయ్యింది: {response.get('message', 'Unknown Error')}")
            
    else:
        # టోకెన్ లేదు, auth_code కూడా లేదు కాబట్టి లాగిన్ లింక్ చూపించాలి
        auth_url = session.generate_authcode()
        st.markdown(f"### 🔐 [Fyers కి లాగిన్ అవ్వడానికి ఇక్కడ క్లిక్ చేయండి]({auth_url})")
        st.warning("ట్రేడింగ్ ఫీచర్స్ వాడటానికి పైన ఉన్న లింక్ ద్వారా లాగిన్ అవ్వండి.")

# 4. లాగిన్ సక్సెస్ అయ్యాక చూపించే స్క్రీన్ (టెస్టింగ్ కోసం)
if "access_token" in st.session_state:
    st.success("✅ మీరు సక్సెస్ ఫుల్ గా లాగిన్ అయ్యారు!")
    
    # Fyers మోడల్ ని ఇనిషియలైజ్ చేయడం
    fyers = fyersModel.FyersModel(
        client_id=client_id, 
        is_async=False, 
        token=st.session_state["access_token"], 
        log_path=""
    )
    
    st.subheader("👤 అకౌంట్ వివరాలు (Connection Test)")
    
    # కనెక్షన్ టెస్ట్ చేయడానికి బటన్
    if st.button("నా ప్రొఫైల్ వివరాలు చూపించు"):
        try:
            profile = fyers.get_profile()
            if profile['s'] == 'ok':
                st.write(f"**పేరు:** {profile['data']['name']}")
                st.write(f"**యూజర్ ఐడి:** {profile['data']['display_name']}")
                st.balloons() # సక్సెస్ అయితే బెలూన్స్ వస్తాయి!
            else:
                st.error(f"ప్రొఫైల్ వివరాలు తీసుకురావడంలో ఎర్రర్: {profile}")
        except Exception as e:
            st.error(f"కనెక్షన్ ఎర్రర్: {e}")
            
    st.divider()
    st.write("🔧 మీ ఆల్గో ట్రేడింగ్ స్ట్రాటజీ (బై/సెల్ లాజిక్) తదుపరి స్టెప్స్ లో ఇక్కడ రాస్తాం.")

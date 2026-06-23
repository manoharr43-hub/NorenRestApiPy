import streamlit as st
# మనం రాసిన సపరేట్ ఫైల్ నుండి లాగిన్ ఫంక్షన్ ని తెచ్చుకుంటున్నాం
from shoonya_login import login_to_shoonya 

st.set_page_config(page_title="NSE AI PRO", layout="wide")

st.title("📈 NSE AI PRO - Trading Dashboard")

st.write("షూన్యా బ్రోకర్ కి కనెక్ట్ అవ్వడానికి కింద క్లిక్ చేయండి:")

# బటన్ నొక్కినప్పుడు లాగిన్ అవ్వడానికి లాజిక్
if st.button("🔑 Login to Shoonya"):
    with st.spinner("కనెక్ట్ అవుతోంది... దయచేసి వేచి ఉండండి"):
        api = login_to_shoonya()
        
        if api:
            st.success("✅ సక్సెస్! Shoonya బ్రోకర్ కి కనెక్ట్ అయ్యారు.")
            st.balloons() # కనెక్ట్ అవ్వగానే బెలూన్స్ వస్తాయి
        else:
            st.error("❌ లాగిన్ ఫెయిల్ అయ్యింది. దయచేసి .env ఫైల్ లో డీటెయిల్స్ చెక్ చేయండి.")

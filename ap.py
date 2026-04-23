import streamlit as st
import pyotp
from NorenRestApiPy import NorenApi

# =========================
# SHOONYA API CLASS
# =========================
class ShoonyaApiPy(NorenApi):
    def __init__(self):
        super().__init__(
            host='https://api.shoonya.com/NorenWS/',
            websocket='wss://api.shoonya.com/NorenWSTP/'
        )

api = ShoonyaApiPy()

# =========================
# STREAMLIT UI
# =========================
st.title("📊 Shoonya Trading Login App")

# =========================
# INPUTS (DO NOT HARDCODE)
# =========================
user_id = st.text_input("User ID")
password = st.text_input("Password", type="password")
vendor_code = st.text_input("Vendor Code")
api_secret = st.text_input("API Secret")
imei = st.text_input("IMEI")

# =========================
# LOGIN BUTTON
# =========================
if st.button("Login"):

    try:
        # 🔥 AUTO TOTP GENERATION (IMPORTANT FIX)
        totp = pyotp.TOTP(api_secret).now()

        api.login(
            userid=user_id,
            password=password,
            twoFA=totp,
            vendor_code=vendor_code,
            imei=imei
        )

        st.success("✅ Login Success!")

        st.write("TOTP Generated:", totp)

    except Exception as e:
        st.error(f"Login Error: {e}")

import streamlit as st
import pyotp
from NorenRestApiPy import NorenApi

# =========================
# SHOONYA API CLASS
# =========================
class ShoonyaApiPy(NorenApi):
    def __init__(self):
        # ✅ No extra arguments
        super().__init__()

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
api_secret = st.text_input("API Secret")   # broker provided
imei = st.text_input("IMEI")
totp_key = st.text_input("TOTP Secret Key")  # from QR code

# =========================
# LOGIN BUTTON
# =========================
if st.button("Login"):

    try:
        # ✅ Generate current OTP from TOTP secret
        totp = pyotp.TOTP(totp_key).now()

        ret = api.login(
            userid=user_id,
            password=password,
            twoFA=totp,              # current OTP
            vendor_code=vendor_code,
            api_secret=api_secret,   # broker API secret
            imei=imei
        )

        if ret and ret.get("stat") == "Ok":
            st.success("✅ Login Success!")
            st.write("TOTP Generated:", totp)
        else:
            st.error(f"Login Failed: {ret}")

    except Exception as e:
        st.error(f"Login Error: {e}")

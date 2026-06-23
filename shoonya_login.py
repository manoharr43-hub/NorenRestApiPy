import pyotp
import logging
import os
from NorenRestApiPy.NorenApi import NorenApi
from dotenv import load_dotenv

# ఎర్రర్స్ తెలుసుకోవడానికి లాగింగ్ సెటప్
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Shoonya API క్లాస్ సెటప్
class ShoonyaApiPy(NorenApi):
    def __init__(self):
        NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/',
                          websocket='wss://api.shoonya.com/NorenWSTP/')

def login_to_shoonya():
    # .env ఫైల్ నుండి మీ సీక్రెట్ కీలను లోడ్ చేయడం
    load_dotenv()

    # మీ అకౌంట్ డీటెయిల్స్ (API Keys)
    user        = os.getenv('SHOONYA_USER')
    pwd         = os.getenv('SHOONYA_PWD')
    vc          = os.getenv('SHOONYA_VC')
    app_key     = os.getenv('SHOONYA_API_KEY')
    imei        = os.getenv('SHOONYA_IMEI', 'abc1234')
    totp_secret = os.getenv('SHOONYA_TOTP_SECRET')

    # డీటెయిల్స్ లేకపోతే ముందే ఆపేయడం
    if not all([user, pwd, vc, app_key, totp_secret]):
        logging.error("❌ క్రెడెన్షియల్స్ మిస్ అయ్యాయి! దయచేసి .env ఫైల్ చెక్ చేసుకోండి.")
        return None

    # pyotp ద్వారా TOTP ని ఆటోమేటిక్ గా జనరేట్ చేయడం
    try:
        totp = pyotp.TOTP(totp_secret).now()
    except Exception as e:
        logging.error(f"❌ TOTP జనరేట్ అవ్వలేదు: {e}")
        return None

    # API కనెక్ట్ చేయడం
    api = ShoonyaApiPy()

    # లాగిన్ ప్రాసెస్
    try:
        login_response = api.login(userid=user, password=pwd, twoFA=totp, vendor_code=vc, api_secret=app_key, imei=imei)
        
        if login_response and login_response.get('stat') == 'Ok':
            logging.info(f"✅ లాగిన్ సక్సెస్! Shoonya లో {user} అకౌంట్ తో కనెక్ట్ అయ్యారు.")
            return api
        else:
            logging.error(f"❌ లాగిన్ ఫెయిల్ అయ్యింది: {login_response}")
            return None
            
    except Exception as e:
        logging.error(f"❌ సర్వర్ ఎర్రర్: {e}")
        return None

# ఫైల్ రన్ చేసినప్పుడు లాగిన్ చెక్ చేయడానికి
if __name__ == '__main__':
    print("Shoonya లాగిన్ స్టార్ట్ అవుతోంది...")
    api = login_to_shoonya()
    
    if api:
        print("🎉 సూపర్! Shoonya API కనెక్షన్ సక్సెస్ ఫుల్ గా పూర్తయింది.")
    else:
        print("⚠️ లాగిన్ అవ్వలేదు, డీటెయిల్స్ చెక్ చేయండి.")

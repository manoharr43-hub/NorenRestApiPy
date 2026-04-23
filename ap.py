import requests
import websocket
import json

class NorenApi:

    def __init__(self, host, websocket):
        self.host = host
        self.websocket_url = websocket
        self.ws = None

    def login(self, userid, password, twoFA, vendor_code, api_secret, imei):
        url = self.host + "QuickAuth"
        payload = {
            "uid": userid,
            "pwd": password,
            "factor2": twoFA,
            "vc": vendor_code,
            "appkey": api_secret,
            "imei": imei
        }

        res = requests.post(url, data=payload)
        return res.json()

    def start_websocket(self, subscribe_callback=None):
        def on_message(ws, message):
            data = json.loads(message)
            if subscribe_callback:
                subscribe_callback(data)

        self.ws = websocket.WebSocketApp(
            self.websocket_url,
            on_message=on_message
        )

        import threading
        thread = threading.Thread(target=self.ws.run_forever)
        thread.daemon = True
        thread.start()

    def subscribe(self, tokens):
        msg = {
            "t": "t",
            "k": "#".join(tokens)
        }
        self.ws.send(json.dumps(msg))

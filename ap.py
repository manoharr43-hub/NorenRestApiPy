import streamlit as st
import requests

CONFIG

API_KEY = "YOUR_API_KEY_HERE"
RADIUS = 3000

st.set_page_config(page_title="Nearby Finder PRO", layout="wide")
st.title("📍 Nearby Finder PRO")

Get user location (IP based)

def get_my_location():
try:
res = requests.get("https://ipinfo.io").json()
loc = res.get("loc", "17.3850,78.4867").split(",")
return float(loc[0]), float(loc[1])
except:
return 17.3850, 78.4867

lat, lng = get_my_location()

st.success(f"📍 Location: {lat}, {lng}")

Distance calculation

def calculate_distance(lat1, lon1, lat2, lon2):
return ((lat1 - lat2)**2 + (lon1 - lon2)**2)**0.5 * 111

Get places

def get_places(place_type):
url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={RADIUS}&type={place_type}&key={API_KEY}"

response = requests.get(url)
data = response.json()

places = []

if "results" in data:
    for place in data["results"]:
        name = place.get("name", "No Name")
        location = place["geometry"]["location"]

        dist = calculate_distance(lat, lng, location["lat"], location["lng"])

        places.append({
            "name": name,
            "distance": round(dist, 2)
        })

places = sorted(places, key=lambda x: x["distance"])
return places[:10]

Button action

if st.button("🔍 Find Nearby Places"):

col1, col2 = st.columns(2)

with col1:
    st.subheader("🍽 Restaurants")
    for p in get_places("restaurant"):
        st.write(f"{p['name']} - {p['distance']} km")

    st.subheader("⛽ Petrol Pumps")
    for p in get_places("gas_station"):
        st.write(f"{p['name']} - {p['distance']} km")

with col2:
    st.subheader("🏨 Lodges")
    for p in get_places("lodging"):
        st.write(f"{p['name']} - {p['distance']} km")

st.caption("Nearby Finder App")

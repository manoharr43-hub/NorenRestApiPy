import streamlit as st
import requests

=========================

CONFIG

=========================

API_KEY = "YOUR_API_KEY_HERE"
RADIUS = 3000

st.set_page_config(page_title="Nearby Finder PRO", layout="wide")
st.title("📍 Nearby Finder PRO")

=========================

AUTO LOCATION (IP BASED)

=========================

def get_my_location():
try:
res = requests.get("https://ipinfo.io").json()
loc = res["loc"].split(",")
return float(loc[0]), float(loc[1])
except:
return None, None

lat, lng = get_my_location()

if lat and lng:
st.success(f"Detected Location: {lat}, {lng}")
else:
st.warning("Location detect avvaledu, manual enter cheyyandi")
lat = st.number_input("Latitude", value=17.3850)
lng = st.number_input("Longitude", value=78.4867)

=========================

DISTANCE CALCULATION

=========================

def calculate_distance(lat1, lon1, lat2, lon2):
return ((lat1 - lat2)**2 + (lon1 - lon2)**2)**0.5 * 111

=========================

GET PLACES

=========================

def get_places(place_type):
url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={RADIUS}&type={place_type}&key={API_KEY}"
response = requests.get(url).json()

places = []

if "results" in response:
    for place in response["results"]:
        name = place.get("name")
        location = place["geometry"]["location"]
        dist = calculate_distance(lat, lng, location["lat"], location["lng"])

        places.append({
            "name": name,
            "distance": round(dist, 2)
        })

# Sort by distance
places = sorted(places, key=lambda x: x["distance"])
return places[:10]

=========================

UI BUTTON

=========================

if st.button("🔍 Find Nearby Places"):

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🍽 Restaurants")
    for p in get_places("restaurant"):
        st.write(f"📍 {p['name']} - {p['distance']} km")

with col2:
    st.subheader("⛽ Petrol Pumps")
    for p in get_places("gas_station"):
        st.write(f"📍 {p['name']} - {p['distance']} km")

with col3:
    st.subheader("🏨 Lodges")
    for p in get_places("lodging"):
        st.write(f"📍 {p['name']} - {p['distance']} km")

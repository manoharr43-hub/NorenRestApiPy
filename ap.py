import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium

API_KEY = "YOUR_API_KEY_HERE"
RADIUS = 3000

st.set_page_config(page_title="Nearby Finder ULTRA", layout="wide")
st.title("Nearby Finder ULTRA")

def get_location():
try:
res = requests.get("https://ipinfo.io").json()
loc = res.get("loc", "17.3850,78.4867").split(",")
return float(loc[0]), float(loc[1])
except:
return 17.3850, 78.4867

lat, lng = get_location()

lat = st.sidebar.number_input("Latitude", value=lat)
lng = st.sidebar.number_input("Longitude", value=lng)

def calc_dist(lat1, lon1, lat2, lon2):
return ((lat1 - lat2)**2 + (lon1 - lon2)**2)**0.5 * 111

def get_places(place_type):
url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={RADIUS}&type={place_type}&key={API_KEY}"
data = requests.get(url).json()

results = []

if "results" in data:
    for p in data["results"]:
        name = p.get("name", "No Name")
        rating = p.get("rating", 0)
        loc = p["geometry"]["location"]

        dist = calc_dist(lat, lng, loc["lat"], loc["lng"])

        results.append({
            "Name": name,
            "Rating": rating,
            "Distance": round(dist, 2),
            "Lat": loc["lat"],
            "Lng": loc["lng"]
        })

df = pd.DataFrame(results)
if not df.empty:
    df = df.sort_values("Distance").head(10)

return df

if st.button("Find Nearby"):

types = {
    "Restaurants": "restaurant",
    "Petrol Pumps": "gas_station",
    "Lodges": "lodging"
}

for title, t in types.items():

    st.subheader(title)
    df = get_places(t)

    if not df.empty:
        st.dataframe(df[["Name", "Rating", "Distance"]])

        m = folium.Map(location=[lat, lng], zoom_start=13)

        folium.Marker([lat, lng], popup="You").add_to(m)

        for _, row in df.iterrows():
            folium.Marker(
                [row["Lat"], row["Lng"]],
                popup=f"{row['Name']} ({row['Distance']} km)"
            ).add_to(m)

        st_folium(m, width=700, height=400)
    else:
        st.write("No data found")

st.write("App Ready")

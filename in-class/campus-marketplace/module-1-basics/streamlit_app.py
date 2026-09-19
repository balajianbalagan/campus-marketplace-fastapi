"""
A minimal front end for Campus Marketplace.

Run the API first (uvicorn app.main:app --reload), then in another terminal:
    streamlit run streamlit_app.py

This is plain Streamlit: it just calls the same REST API you built in app/main.py
using the `requests` library. No new backend concepts here -- this is purely
"what does a person clicking buttons see instead of Swagger."
"""

import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.title("🛒 Campus Marketplace")

# --- form to add a new listing ---
st.header("Sell something")
with st.form("new_listing"):
    title = st.text_input("What are you selling?")
    price = st.number_input("Price ($)", min_value=0.0, step=0.5)
    seller_name = st.text_input("Your name")
    submitted = st.form_submit_button("Post listing")

    if submitted:
        response = requests.post(f"{API_URL}/listings", json={
            "title": title,
            "price_cents": int(price * 100),
            "seller_name": seller_name,
        })
        if response.status_code == 200:
            st.success("Listed!")
        else:
            st.error(f"Something went wrong: {response.text}")

# --- show everything for sale ---
st.header("What's for sale")
listings = requests.get(f"{API_URL}/listings").json()

if not listings:
    st.write("Nothing listed yet -- be the first!")
else:
    for listing in listings:
        price_dollars = listing["price_cents"] / 100
        st.write(f"**{listing['title']}** — ${price_dollars:.2f} — sold by {listing['seller_name']}")

import requests
import streamlit as st

st.title("Campus Marketplace")
with st.form("listing"):
    title = st.text_input("Title")
    description = st.text_area("Description")
    price = st.number_input("Price (INR)", min_value=0.0)
    seller = st.text_input("Seller")
    if st.form_submit_button("Post"):
        response = requests.post("http://127.0.0.1:8000/listings", json={
            "title": title, "description": description, "price_cents": int(price * 100), "seller_name": seller,
        }, timeout=5)
        st.success("Posted") if response.status_code == 201 else st.error(response.text)

response = requests.get("http://127.0.0.1:8000/listings", timeout=5)
if response.ok:
    for listing in response.json():
        st.write(f"**{listing['title']}** - INR {listing['price_cents'] / 100:.2f}")

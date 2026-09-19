# requests sends HTTP calls to the FastAPI API; Streamlit renders browser controls.
import requests
import streamlit as st

# This heading appears at the top of the Streamlit page.
st.title("Campus Marketplace")
# A form batches its widget values and submits them together when Post is clicked.
with st.form("listing"):
    # Each widget returns the value the visitor typed or selected.
    title = st.text_input("Title")
    description = st.text_area("Description")
    price = st.number_input("Price (INR)", min_value=0.0)
    seller = st.text_input("Seller")
    # The indented code runs only when the user submits this form.
    if st.form_submit_button("Post"):
        # POST JSON to FastAPI; the UI does not access the SQLite file itself.
        response = requests.post("http://127.0.0.1:8000/listings", json={
            "title": title, "description": description, "price_cents": int(price * 100), "seller_name": seller,
        }, timeout=5)
        # Show a clear success message or the API error body.
        st.success("Posted") if response.status_code == 201 else st.error(response.text)

# Fetch the current listings whenever Streamlit reruns the script.
response = requests.get("http://127.0.0.1:8000/listings", timeout=5)
# Only try to read JSON after FastAPI returns a successful HTTP response.
if response.ok:
    # Loop over the JSON array and render one line per listing.
    for listing in response.json():
        # Divide paise by 100 only for the display price.
        st.write(f"**{listing['title']}** - INR {listing['price_cents'] / 100:.2f}")

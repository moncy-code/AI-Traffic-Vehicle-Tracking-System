import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Vehicle Tracking Dashboard", layout="wide")

st.title("Smart Vehicle Tracking System")
st.write("Search a vehicle by registration number and view its last seen location and history.")

plate_number = st.text_input("Enter registration number")

if st.button("Search"):
    if not plate_number.strip():
        st.warning("Please enter a registration number.")
    else:
        cleaned_plate = plate_number.strip().upper().replace(" ", "")

        try:
            last_seen_response = requests.get(
                f"{API_URL}/vehicle/{cleaned_plate}/last-seen"
            )
            history_response = requests.get(
                f"{API_URL}/vehicle/{cleaned_plate}"
            )
            prediction_response = requests.get(
                f"{API_URL}/vehicle/{cleaned_plate}/predict"
            )

        except requests.exceptions.ConnectionError:
            st.error("Backend server is not running.")
            st.stop()

        # ---------------- LAST SEEN ----------------
        if last_seen_response.status_code == 200:
            last_seen = last_seen_response.json()

            st.subheader("Last Seen")
            col1, col2, col3 = st.columns(3)
            col1.metric("Plate Number", last_seen["plate_number"])
            col2.metric("Camera ID", last_seen["camera_id"])
            col3.metric("Time", last_seen["timestamp"])

        else:
            st.warning("No last-seen data found.")

        # ---------------- HISTORY ----------------
        if history_response.status_code == 200:
            history = history_response.json()
            df = pd.DataFrame(history)

            st.subheader("Sighting History")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No history found for this plate number.")

        # ---------------- PREDICTION ----------------
        if prediction_response.status_code == 200:
            prediction = prediction_response.json()

            st.subheader("Predicted Next Location")

            st.success(
                f"Next likely camera: {prediction['predicted_camera']} "
                f"({prediction['probability']*100:.0f}% confidence)"
            )
        else:
            st.info("Not enough data for prediction.")
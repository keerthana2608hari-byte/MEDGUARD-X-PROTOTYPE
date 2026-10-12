import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="MEDGUARD-X",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 MEDGUARD-X")
st.subheader("AI Medication Stability & Inventory Management")

st.success("Your application is working!")

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a page",
    ["Dashboard", "Add Medication", "Inventory"]
)

if "medicines" not in st.session_state:
    st.session_state.medicines = []

if page == "Dashboard":
    st.header("Medication Dashboard")
    st.write("Monitor your medication inventory and expiry dates.")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Medicines", len(st.session_state.medicines))

    with col2:
        st.metric(
            "Expiring Soon",
            sum(
                0 <= (m["Expiry Date"] - date.today()).days <= 30
                for m in st.session_state.medicines
            )
        )

elif page == "Add Medication":
    st.header("Add New Medication")

    with st.form("medicine_form"):
        name = st.text_input("Medication Name")
        quantity = st.number_input("Quantity", min_value=1, step=1)
        expiry = st.date_input("Expiry Date", min_value=date.today())
        temperature = st.number_input(
            "Storage Temperature (°C)",
            value=25.0
        )

        submitted = st.form_submit_button("Add Medication")

        if submitted:
            if name.strip():
                st.session_state.medicines.append({
                    "Name": name.strip(),
                    "Quantity": quantity,
                    "Expiry Date": expiry,
                    "Temperature (°C)": temperature
                })
                st.success(f"{name} added successfully!")
            else:
                st.error("Please enter a medication name.")

elif page == "Inventory":
    st.header("Medication Inventory")

    if st.session_state.medicines:
        df = pd.DataFrame(st.session_state.medicines)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No medicines added yet. Go to Add Medication.")
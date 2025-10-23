# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import csv

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE
st.title("Screen Time Survey")

# DATA INPUT FORM
with st.form("survey_form"):
    # Dropdown to select day
    day = st.selectbox( #NEW
        "Select day:",
        options=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )

    # Number input for hours (with +/- buttons)
    hours = st.number_input( #NEW
        "Enter screen time hours:",
        min_value=0.0,
        max_value=24.0,
        value=0.0,
        step=0.5
    )

    # Submit button
    submitted = st.form_submit_button("Submit Data")

    # When submitted, write to CSV
    if submitted:
        with open('data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([day, hours])

        st.success("Data submitted!")

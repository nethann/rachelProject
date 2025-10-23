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
st.write("Enter your screen time hours for each day of the week:")

# DATA INPUT FORM
with st.form("survey_form"):
    # Number inputs for each day of the week
    mon_hours = st.number_input("Monday hours of screen time", min_value=0.0, max_value=24.0, value=0.0, step=0.5) #NEW
    tue_hours = st.number_input("Tuesday hours of screen time", min_value=0.0, max_value=24.0, value=0.0, step=0.5) #NEW
    wed_hours = st.number_input("Wednesday hours of screen time", min_value=0.0, max_value=24.0, value=0.0, step=0.5) #NEW
    thu_hours = st.number_input("Thursday hours of screen time", min_value=0.0, max_value=24.0, value=0.0, step=0.5) #NEW
    fri_hours = st.number_input("Friday hours of screen time", min_value=0.0, max_value=24.0, value=0.0, step=0.5) #NEW
    sat_hours = st.number_input("Saturday hours of screen time", min_value=0.0, max_value=24.0, value=0.0, step=0.5) #NEW
    sun_hours = st.number_input("Sunday hours of screen time", min_value=0.0, max_value=24.0, value=0.0, step=0.5) #NEW

    # Submit button
    submitted = st.form_submit_button("Submit All Data")

    # When submitted, write all days to CSV
    if submitted:
        # Create list of all days and hours
        days_data = [
            ("Monday", mon_hours),
            ("Tuesday", tue_hours),
            ("Wednesday", wed_hours),
            ("Thursday", thu_hours),
            ("Friday", fri_hours),
            ("Saturday", sat_hours),
            ("Sunday", sun_hours)
        ]

        # Write to CSV (overwrite mode to replace old data)
        with open('data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(['Category', 'Value'])
            # Write all days
            for day, hours in days_data:
                writer.writerow([day, hours])

        st.success("Data submitted for all 7 days!")

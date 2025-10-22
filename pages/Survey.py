# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).
import csv # For proper CSV handling with commas

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Screen Time Survey 📝")
st.write("Track your daily screen time by entering the date and hours spent on screens.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    category_input = st.text_input("Enter the date (e.g., Monday, Oct 21, Week 1):")
    value_input = st.text_input("Enter screen time in hours (e.g., 5.5):")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        # Validate that both fields have data
        if category_input and value_input:
            # Append to the CSV file using proper CSV writer (handles commas correctly)
            with open('data.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([category_input, value_input])

            st.success("Your data has been submitted!")
            st.write(f"You entered: **Category:** {category_input}, **Value:** {value_input}")
        else:
            st.error("Please fill in both fields before submitting.")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json
import os

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations")

# Load CSV data
csv_data = None
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    try:
        csv_data = pd.read_csv('data.csv')
    except Exception as e:
        st.error(f"Error loading CSV: {e}")

# Load JSON data
json_data = None
if os.path.exists('data.json'):
    try:
        with open('data.json', 'r') as file:
            json_data = json.load(file)
    except Exception as e:
        st.error(f"Error loading JSON: {e}")

st.divider()

# Display CSV data table
st.header("Current Data in CSV")
if csv_data is not None and len(csv_data) > 0:
    st.dataframe(csv_data, use_container_width=True)
else:
    st.info("No CSV data available yet.")

st.divider()

# ==================== GRAPH 1: STATIC (JSON) ====================
st.subheader("Static: Daily Screen Time by Activity")
st.write("This bar chart shows screen time breakdown by activity type.")

if json_data:
    labels = [item['label'] for item in json_data['data_points']]
    hours = [item['hours'] for item in json_data['data_points']]

    chart_data = pd.DataFrame({
        'Activity': labels,
        'Hours': hours
    })

    st.bar_chart(chart_data.set_index('Activity'))
else:
    st.warning("No JSON data available.")

st.divider()

# ==================== GRAPH 2: DYNAMIC (CSV) ====================
st.subheader("Dynamic: Weekly Screen Time Trend")
st.write("This line chart shows screen time over days. Use the controls to filter and view the data.")

if csv_data is not None and len(csv_data) > 0:
    # Session state for slider
    if 'num_days' not in st.session_state:
        st.session_state.num_days = min(7, len(csv_data))

    # Session state for min hours
    if 'min_hours_line' not in st.session_state:
        st.session_state.min_hours_line = 0.0

    # Slider for number of days
    num_to_show = st.slider( #NEW
        "Number of days to display:",
        min_value=1,
        max_value=len(csv_data),
        value=st.session_state.num_days,
        key='days_slider'
    )

    st.session_state.num_days = num_to_show

    # Slider for minimum hours filter
    min_hours_filter = st.slider( #NEW
        "Filter by minimum screen time (hours):",
        min_value=0.0,
        max_value=10.0,
        value=st.session_state.min_hours_line,
        step=0.5,
        key='line_hours_filter'
    )

    st.session_state.min_hours_line = min_hours_filter

    # Filter data by number of days first
    filtered_data = csv_data.head(num_to_show)

    # Then filter by minimum hours
    filtered_data = filtered_data[filtered_data['Value'] >= min_hours_filter]

    if len(filtered_data) > 0:
        chart_data = filtered_data.set_index('Category')
        st.line_chart(chart_data)
    else:
        st.info("No days meet the filter criteria.")
else:
    st.warning("No CSV data available.")

st.divider()

# ==================== GRAPH 3: DYNAMIC SCATTER PLOT (JSON) ====================
st.subheader("Dynamic: Time Spent vs How Often Used")
st.write("This scatter plot shows total hours spent on each activity compared to how many times per day you use it. Select activities and adjust the filter to explore the data.")

if json_data:
    # Session state for min hours
    if 'min_hours_scatter' not in st.session_state:
        st.session_state.min_hours_scatter = 0.0

    # Session state for selected activities
    if 'scatter_selected' not in st.session_state:
        st.session_state.scatter_selected = [item['label'] for item in json_data['data_points']]

    # Get all activities
    all_activities = [item['label'] for item in json_data['data_points']]

    # Multiselect for activities
    selected_activities = st.multiselect( #NEW
        "Select activities to compare:",
        options=all_activities,
        default=st.session_state.scatter_selected,
        key='scatter_activity_selector'
    )

    st.session_state.scatter_selected = selected_activities

    # Slider to filter by hours
    min_hours = st.slider( #NEW
        "Minimum hours to display:",
        min_value=0.0,
        max_value=5.0,
        value=st.session_state.min_hours_scatter,
        step=0.5,
        key='scatter_hours_filter'
    )

    st.session_state.min_hours_scatter = min_hours

    # Filter data
    filtered_data = [item for item in json_data['data_points']
                     if item['hours'] >= min_hours and item['label'] in selected_activities]

    if filtered_data:
        hours = [item['hours'] for item in filtered_data]
        sessions = [item['sessions'] for item in filtered_data]

        chart_data = pd.DataFrame({
            'Total Hours': hours,
            'Times Used Per Day': sessions
        })

        # Create scatter plot
        st.scatter_chart(chart_data, x='Total Hours', y='Times Used Per Day') #NEW
    else:
        st.info("No activities meet the filter criteria.")
else:
    st.warning("No JSON data available.")

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
st.subheader("Graph 1: Daily Screen Time by Activity")
st.write("This bar chart shows screen time breakdown by activity type.")

if json_data:
    labels = [item['label'] for item in json_data['data_points']]
    values = [item['value'] for item in json_data['data_points']]

    chart_data = pd.DataFrame({
        'Activity': labels,
        'Hours': values
    })

    st.bar_chart(chart_data.set_index('Activity'))
else:
    st.warning("No JSON data available.")

st.divider()

# ==================== GRAPH 2: DYNAMIC (CSV) ====================
st.subheader("Graph 2: Weekly Screen Time Trend")
st.write("This line chart shows screen time over days. Use the slider to adjust how many days to display.")

if csv_data is not None and len(csv_data) > 0:
    # Session state for slider
    if 'num_days' not in st.session_state:
        st.session_state.num_days = min(7, len(csv_data))

    # Slider
    num_to_show = st.slider( #NEW
        "Number of days:",
        min_value=1,
        max_value=len(csv_data),
        value=st.session_state.num_days,
        key='days_slider'
    )

    st.session_state.num_days = num_to_show

    filtered_data = csv_data.head(num_to_show)
    chart_data = filtered_data.set_index('Category')

    st.line_chart(chart_data)
else:
    st.warning("No CSV data available.")

st.divider()

# ==================== GRAPH 3: DYNAMIC (JSON) ====================
st.subheader("Graph 3: Activity Comparison")
st.write("Select which activities to compare.")

if json_data:
    # Session state for multiselect
    if 'selected_activities' not in st.session_state:
        st.session_state.selected_activities = [item['label'] for item in json_data['data_points']]

    all_activities = [item['label'] for item in json_data['data_points']]

    # Multiselect
    selected = st.multiselect( #NEW
        "Select activities:",
        options=all_activities,
        default=st.session_state.selected_activities,
        key='activity_selector'
    )

    st.session_state.selected_activities = selected

    if selected:
        filtered_json = [item for item in json_data['data_points'] if item['label'] in selected]

        chart_data = pd.DataFrame({
            'Activity': [item['label'] for item in filtered_json],
            'Hours': [item['value'] for item in filtered_json]
        })

        st.bar_chart(chart_data.set_index('Activity'))
    else:
        st.info("Select at least one activity.")
else:
    st.warning("No JSON data available.")

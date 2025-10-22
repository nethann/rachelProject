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

# PAGE TITLE AND INFORMATION
st.title("Screen Time Data Visualizations 📈")
st.write("This page displays graphs based on the collected screen time data.")

# DATA LOADING
st.divider()
st.header("Load Data")

# Load CSV data
csv_data = None
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    try:
        csv_data = pd.read_csv('data.csv')
        st.success(f"✓ CSV data loaded successfully! ({len(csv_data)} rows)")
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
else:
    st.warning("CSV file is empty or doesn't exist. Please add data using the Survey page.")

# Load JSON data
json_data = None
if os.path.exists('data.json'):
    try:
        with open('data.json', 'r') as file:
            json_data = json.load(file)
        st.success(f"✓ JSON data loaded successfully! ({len(json_data['data_points'])} data points)")
    except Exception as e:
        st.error(f"Error loading JSON: {e}")
else:
    st.warning("JSON file doesn't exist.")

# GRAPH CREATION
st.divider()
st.header("Graphs")

# ==================== GRAPH 1: STATIC GRAPH (JSON DATA) ====================
st.subheader("Graph 1: Daily Screen Time by Activity")
st.write("This bar chart shows how daily screen time is distributed across different activities.")

if json_data:
    # Extract labels and values from JSON
    labels = [item['label'] for item in json_data['data_points']]
    values = [item['value'] for item in json_data['data_points']]

    # Create DataFrame for plotting
    chart_data = pd.DataFrame({
        'Activity': labels,
        'Hours': values
    })

    # Display as bar chart (static)
    st.bar_chart(chart_data.set_index('Activity')) #NEW
else:
    st.warning("No JSON data available to display.")

st.divider()

# ==================== GRAPH 2: DYNAMIC GRAPH (CSV DATA) ====================
st.subheader("Graph 2: Screen Time Trend (Interactive)")
st.write("This line chart shows screen time over different days. Use the slider to filter the number of entries displayed.")

if csv_data is not None and len(csv_data) > 0:
    # Initialize session state for the slider
    if 'num_entries' not in st.session_state: #NEW
        st.session_state.num_entries = min(5, len(csv_data))

    # Slider to select number of entries to display
    num_to_show = st.slider( #NEW
        "Number of entries to display:",
        min_value=1,
        max_value=len(csv_data),
        value=st.session_state.num_entries,
        key='entries_slider'
    )

    # Update session state
    st.session_state.num_entries = num_to_show

    # Filter data based on slider
    filtered_data = csv_data.head(num_to_show)

    # Prepare data for line chart
    chart_data = filtered_data.set_index('Category')

    # Display line chart
    st.line_chart(chart_data) #NEW

    # Show the data table
    st.write(f"Showing {num_to_show} of {len(csv_data)} entries:")
    st.dataframe(filtered_data) #NEW
else:
    st.warning("No CSV data available. Please add data using the Survey page.")

st.divider()

# ==================== GRAPH 3: DYNAMIC GRAPH (JSON DATA) ====================
st.subheader("Graph 3: Activity Comparison (Interactive)")
st.write("Select which activities to compare. This allows you to focus on specific screen time categories.")

if json_data:
    # Initialize session state for selected activities
    if 'selected_activities' not in st.session_state:
        # Default: select all activities
        st.session_state.selected_activities = [item['label'] for item in json_data['data_points']]

    # Get all available activities
    all_activities = [item['label'] for item in json_data['data_points']]

    # Multiselect widget for choosing activities
    selected = st.multiselect( #NEW
        "Select activities to display:",
        options=all_activities,
        default=st.session_state.selected_activities,
        key='activity_selector'
    )

    # Update session state
    st.session_state.selected_activities = selected

    if selected:
        # Filter JSON data based on selection
        filtered_json = [item for item in json_data['data_points'] if item['label'] in selected]

        # Create DataFrame for plotting
        chart_data = pd.DataFrame({
            'Activity': [item['label'] for item in filtered_json],
            'Hours': [item['value'] for item in filtered_json]
        })

        # Display as bar chart
        st.bar_chart(chart_data.set_index('Activity'))

        # Show total hours for selected activities
        total_hours = sum([item['value'] for item in filtered_json])
        st.metric("Total Screen Time (Selected Activities)", f"{total_hours} hours") #NEW
    else:
        st.info("Please select at least one activity to display.")
else:
    st.warning("No JSON data available to display.")

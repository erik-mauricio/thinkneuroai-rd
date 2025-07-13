import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from CsvReader import CsvReader
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'component-template'))
from my_component import my_component
# Page configuration
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# Custom CSS for navigation styling
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        font-size: 18px !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        font-size: 20px !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-size: 24px !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize data reader
@st.cache_resource
def load_data():
    return CsvReader("merged_student_data.csv")

reader = load_data()

# Header with logo
with open("thinkneuro-logo.png", "rb") as f:
    encoded = base64.b64encode(f.read()).decode()

st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 5px;">
        <img src="data:image/png;base64,{encoded}" width="100" style="margin-right: 15px;">
        <div>
            <h1 style="margin: 0;">ThinkNeuro</h1>
            <p style="margin: 0;">Doctor Discover Program</p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.divider()

# Dashboard title and export button
col1, col2 = st.columns([8, 2])
with col1:
    st.title("Student Dashboard")

# Filters section
with st.container(border=True):
    col1, col2, col3, = st.columns(3)

    with col1:
        st.markdown("**Grade**")
        grade = st.selectbox(
            "Grade",
            ["All Grades", "9th", "10th", "11th", "12th"],
            label_visibility="collapsed"
        )

    with col2:
        st.markdown("**Cohort**")
        cohort = st.selectbox(
            "Cohort",
            ["All Cohorts", "Spring 2025", "Fall 2024"],
            label_visibility="collapsed"
        )

    with col3:
        st.markdown("**Region**")
        region = st.selectbox(
            "Region",
            ["All Regions", "East", "West", "Central"],
            label_visibility="collapsed"
        )

# Get filtered data for export
filtered_data = reader.filter_data(grade, cohort, region)

# Convert filtered data to CSV for download
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv_data = convert_df_to_csv(filtered_data)

# Create filename based on active filters
filename_parts = ["student_data"]
if grade != "All Grades":
    filename_parts.append(grade.replace("th", ""))
if cohort != "All Cohorts":
    filename_parts.append(cohort.replace(" ", "_"))
if region != "All Regions":
    filename_parts.append(region)

filename = "_".join(filename_parts) + ".csv"

# Export button with filtered data
with col2:
    st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
    st.download_button(
        label="Export CSV",
        data=csv_data,
        file_name=filename,
        mime="text/csv",
        use_container_width=True
    )

# Display active filters
active_filters = []
if grade != "All Grades":
    active_filters.append(grade)
if cohort != "All Cohorts":
    active_filters.append(cohort)
if region != "All Regions":
    active_filters.append(region)

if active_filters:
    st.info(f"🔍 Active filters: {', '.join(active_filters)}")

# Get filtered metrics
metrics = reader.get_student_metrics(grade, cohort, region)
pvsa_count = reader.get_pvsa_eligible_count(grade, cohort, region)
kits_delivered = reader.get_kits_delivered_count(grade, cohort, region)
kits_pending = reader.get_kits_pending_count(grade, cohort, region)

# Metrics cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    my_component(
        title="Total Students",
        value=str(metrics['total_students']),
        delta="+5.4%",
        caption="Compared to last month",
        key="1"
    )

with col2:
    my_component(
        title="Active Students",
        value=str(metrics['active_students']),
        delta="",
        caption=f"{metrics['active_percentage']}% of total enrollment",
        key="2"
    )

with col3:
    my_component(
        title="Kits Delivered",
        value=str(kits_delivered),
        delta="",
        caption=f"{kits_pending} kits still pending",
        key="3"
    )

with col4:
    my_component(
        title="PVSA Eligible",
        value=str(pvsa_count),
        delta="+12.8%",
        caption="25% of students",
        key="4"
    )

# Charts section
st.markdown("### Analytics")

col1, col2 = st.columns(2)

with col1:
    # Kit tracking pie chart
    kit_data = reader.get_kit_tracking_data()
    kit_chart = px.pie(
        values=kit_data["Value"],
        names=kit_data["Category"],
        title="Kit Tracking"
    )
    st.plotly_chart(kit_chart, use_container_width=True)

with col2:
    # Module completion bar chart
    module_data = reader.get_module_completion_data()
    module_chart = px.bar(
        x=module_data['Completion_Rate'],
        y=module_data['Module'],
        orientation='h',
        title="Module Completion"
    )
    st.plotly_chart(module_chart, use_container_width=True)
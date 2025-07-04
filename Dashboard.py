from random import choice

import streamlit as st
import pandas as pd
import plotly.express as px
from CsvReader import CsvReader
import base64

st.set_page_config(page_title="Dashboard", page_icon="📊")
with open("thinkneuro-logo.png", "rb") as f:
    encoded = base64.b64encode(f.read()).decode()

st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 20px">
        <img src="data:image/png;base64,{encoded}" width="100" style="margin-right: 15px;">
        <div>
            <h1 style="margin: 0;">ThinkNeuro</h1>
            <p style="margin: 0;">Doctor Discover Program</p>
        </div>
    </div>
""", unsafe_allow_html=True)
st.sidebar.markdown("**COHORTS**")
cohort = st.sidebar.radio(
    label="",
    options=["All Cohorts", "Spring 2025", "Fall 2024", "Spring 2024"],
    label_visibility="collapsed"
)


st.write(f"Cohort: {cohort}")

###These columns(cols) are used for the top header section
col1, col2, col3 = st.columns([6, 1, 1])

with col1:
    st.text_input("datasearch", placeholder="Search", label_visibility="collapsed")


st.divider()

with st.container():
    col1, col2, col3 = st.columns([3, 2, 1])

    with col1:
        st.markdown("<div style='margin-top: .3px;'></div>", unsafe_allow_html=True)
        st.header("Student DashBoard")

    with col2:
        choice = st.selectbox("Filter by time", ["Last 30 days", "Last 60 days", "Last 90 days" ])

    with col3:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        st.download_button("Export", "pdf")


with st.container(border=True):
    col1, col2, col3, col4 = st.columns([2.5, 2.5, 2.5, 2.5])

    with col1:
        st.markdown("**Grade**")
        grade = st.selectbox("Grade", ["All Grades", "9th", "10th", "11th", "12th"], label_visibility="collapsed")

    with col2:
        st.markdown("**Cohort**")
        cohort = st.selectbox("Cohort", ["All Cohorts", "Spring 2025", "Fall 2024"], label_visibility="collapsed")

    with col3:
        st.markdown("**Region**")
        region = st.selectbox("Region", ["All Regions", "East", "West", "Central"], label_visibility="collapsed")

    with col4:
        st.markdown("**&nbsp;**")
        apply = st.button("Apply Filters", type="primary")

with st.container():
    reader = CsvReader("student_tracking_template.csv")
    data  = reader.kitTrackingData()

    kitPieChartFigure = px.pie(values=data["Value"], names=data["Category"], title="Kit Tracking")
    st.plotly_chart(kitPieChartFigure)
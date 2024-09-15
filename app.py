import streamlit as st
import pandas as pd
import openai
import os
import plotly.express as px

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Retrieve API key from Streamlit secrets
openai.api_key = st.secrets["api_keys"]["together_api_key"]

# Custom CSS for better styling
def add_custom_styles():
    st.markdown("""
    <style>
        /* Background color */
        body {
            background-color: #f7f9fc;
        }
        /* Customize title and subtitles */
        h1, h2 {
            color: #1F77B4;
            text-align: center;
        }
        /* Box styling */
        .stTextInput, .stNumberInput, .stTextArea {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 2px 2px 15px rgba(0, 0, 0, 0.1);
        }
        /* Form and button styling */
        .stButton>button {
            background-color: #1F77B4;
            color: white;
            padding: 8px 16px;
            border-radius: 5px;
            border: none;
            font-size: 16px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #005082;
        }
        /* Table styling */
        .dataframe {
            border-collapse: collapse;
            width: 100%;
        }
        .dataframe th, .dataframe td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        .dataframe tr:hover {
            background-color: #f1f1f1;
        }
        /* Chart box */
        .stPlotlyChart {
            margin-top: 20px;
            background-color: #f0f3f6;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 15px rgba(0, 0, 0, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)

# Function to clear input fields
def clear_form():
    st.session_state.competitor_name = ""
    st.session_state.market_share = 0.0
    st.session_state.strengths = ""
    st.session_state.weaknesses = ""
    st.session_state.opportunities = ""
    st.session_state.threats = ""

# Initialize session state for competitor data
if 'competitors' not in st.session_state:
    st.session_state.competitors = []

if 'competitor_name' not in st.session_state:
    st.session_state.competitor_name = ""
if 'market_share' not in st.session_state:
    st.session_state.market_share = 0.0
if 'strengths' not in st.session_state:
    st.session_state.strengths = ""
if 'weaknesses' not in st.session_state:
    st.session_state.weaknesses = ""
if 'opportunities' not in st.session_state:
    st.session_state.opportunities = ""
if 'threats' not in st.session_state:
    st.session_state.threats = ""

# Streamlit UI
st.title('💼 AI-Powered Competitive Market Analysis 📊')
st.markdown("""
    Welcome to the **AI-Powered Competitive Market Analysis** tool. This app helps businesses gain deep insights 
    into their competitors and market dynamics using AI. Enter competitor information to generate actionable 
    strategies and recommendations!
""")

# Competitor Input Form
st.subheader('🏢 Enter Competitor Information')
with st.form(key='competitor_form'):
    competitor_name = st.text_input('Competitor Name:', value=st.session_state.competitor_name)
    market_share = st.number_input('Market Share (%):', min_value=0.0, max_value=100.0, value=st.session_state.market_share)
    strengths = st.text_area('Strengths:', value=st.session_state.strengths)
    weaknesses = st.text_area('Weaknesses:', value=st.session_state.weaknesses)
    opportunities = st.text_area('Opportunities:', value=st.session_state.opportunities)
    threats = st.text_area('Threats:', value=st.session_state.threats)
    submit_button = st.form_submit_button('Submit Competitor Data')

    if submit_button:
        if competitor_name and market_share:
            competitor_entry = {
                'name': competitor_name,
                'market_share': market_share,
                'strengths': strengths,
                'weaknesses': weaknesses,
                'opportunities': opportunities,
                'threats': threats
            }
            st.session_state.competitors.append(competitor_entry)
            st.success(f'{competitor_name} added to the competitor list!')
            # Clear the form fields
            clear_form()
        else:
            st.error("Please fill out all required fields.")

# Display Competitor Data
if st.session_state.competitors:
    st.subheader('📊 Competitor Data Overview')
    competitors_df = pd.DataFrame(st.session_state.competitors)
    st.write(competitors_df)

    # Visualize Market Share
    fig = px.pie(competitors_df, names='name', values='market_share', title='Market Share Distribution')
    st.plotly_chart(fig)

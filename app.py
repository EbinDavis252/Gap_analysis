# app.py

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from nlp_extractor import extract_skills # Import your skill extractor

# --- Database Connection ---
@st.cache_resource
def get_db_connection():
    return sqlite3.connect('jobs.db', check_same_thread=False)

# --- Page Configuration ---
st.set_page_config(
    page_title="Dynamic Skill Gap Analyzer",
    page_icon="🤖",
    layout="wide"
)

# --- Main App ---
st.title("Dynamic Curriculum and Skill Gap Analysis Tool")
st.markdown("This tool analyzes real-time job market data to identify in-demand skills and helps bridge the gap between academic curricula and industry needs.")

# --- Sidebar for User Input ---
st.sidebar.header("Analyze Your Curriculum")
# In a real app, you would load this from a database or file.
# For this demo, we use a predefined list of skills for a sample curriculum.
sample_curriculum_skills = st.sidebar.text_area(
    "Enter skills taught in your curriculum (comma-separated):",
    "Python, Java, SQL, Data Structures, Algorithms"
).lower().split(',')
sample_curriculum_skills = [skill.strip() for skill in sample_curriculum_skills]

# --- Dashboard View ---

# Fetch data from the database
conn = get_db_connection()
try:
    # This query joins jobs and skills to count the frequency of each skill
    query = """
        SELECT s.name as skill, COUNT(js.job_id) as count
        FROM skills s
        JOIN job_skills js ON s.id = js.skill_id
        GROUP BY s.name
        ORDER BY count DESC
        LIMIT 20
    """
    top_skills_df = pd.read_sql_query(query, conn)
except pd.io.sql.DatabaseError:
    st.error("Database is empty. Please run the scraper and processor first.")
    st.stop()


# --- Displaying Analytics ---
col1, col2 = st.columns((2, 1.5))

with col1:
    st.header("Top 20 In-Demand Skills")
    if not top_skills_df.empty:
        fig = px.bar(
            top_skills_df,
            x='count',
            y='skill',
            orientation='h',
            title="Frequency of Top Skills in Job Postings",
            labels={'skill': 'Skill', 'count': 'Frequency Count'},
            text='count'
        )
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No skill data found. The database might be empty.")

with col2:
    st.header("Skill Gap Analysis")
    if not top_skills_df.empty:
        market_skills = set(top_skills_df['skill'].str.lower())
        curriculum_skills_set = set(sample_curriculum_skills)

        # Calculate skill gap
        skill_gap = list(market_skills - curriculum_skills_set)
        
        st.subheader("Skills Missing from Your Curriculum:")
        if skill_gap:
            gap_df = pd.DataFrame(skill_gap, columns=["Missing Skills"])
            st.dataframe(gap_df, use_container_width=True)
        else:
            st.success("Excellent! Your curriculum covers all the top in-demand skills.")

        st.subheader("Learning Recommendations:")
        st.info("To bridge this gap, consider adding courses or workshops on the missing skills listed above. Focus on practical projects using technologies like Pandas for data analysis, TensorFlow for machine learning, and AWS for cloud computing.")
    else:
        st.warning("Cannot perform gap analysis without market data.")


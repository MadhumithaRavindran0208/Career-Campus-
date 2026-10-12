"""
CareerCompass AI — Neuro-Symbolic Career Intelligence System
Main Application Entrypoint
"""

import sys
import os
import streamlit as st

# Ensure project root is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui_components import inject_custom_theme
from neuro_symbolic_engine import get_or_create_dataset, train_neuro_symbolic_models
from job_service import get_all_jobs

# Import Modular Views
from views.view_overview import render_overview_page
from views.view_resume_match import render_resume_match_page
from views.view_suggestions import render_suggestions_page
from views.view_live_jobs import render_live_jobs_page
from views.view_evaluation import render_evaluation_page

# Configure Page
st.set_page_config(
    page_title="CareerCompass AI | Neuro-Symbolic Career Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply High-Contrast Modern Theme
inject_custom_theme()

# Cache Data Loading & Model Training
@st.cache_data(show_spinner=False)
def load_cached_dataset():
    return get_or_create_dataset()

@st.cache_resource(show_spinner=False)
def load_cached_models(data_len: int):
    df_src = get_or_create_dataset()
    return train_neuro_symbolic_models(df_src)

df = load_cached_dataset()
results, X_test, y_test = load_cached_models(len(df))
gb_model = results.get("Gradient Boosting", {}).get("model", None)
best_model = gb_model if gb_model is not None else results.get("Random Forest", {}).get("model", None)
all_jobs = get_all_jobs(include_live_feed=False)

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 18px;">
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 22px; font-weight: 700; letter-spacing: -0.03em; color: #F1F5F9;">
            ✦ CareerCompass <span style="color: #3B82F6;">AI</span>
        </div>
        <div style="color: #94A3B8; font-size: 10.5px; letter-spacing: 0.12em; font-weight: 600; text-transform: uppercase; margin-top: 3px;">
            NEURO-SYMBOLIC INTELLIGENCE
        </div>
    </div>
    """, unsafe_allow_html=True)

    nav_page = st.radio(
        "NAVIGATE WORKSPACE",
        [
            "Overview & Architecture",
            "Resume Match & Opportunities",
            "Personalized Suggestions & Roadmap",
            "Live Job Market & LinkedIn",
            "Technical Model Evaluation"
        ],
        index=1  # Default to Resume Match for immediate high user value
    )

    st.markdown("<hr style='margin: 18px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 11px; color: #cbd5e1; text-transform: uppercase; letter-spacing: 0.12em; font-weight: 700;">SYSTEM ENGINE STATUS</div>
    <div style="display: flex; align-items: center; gap: 8px; margin-top: 8px;">
        <span style="height: 9px; width: 9px; background-color: #10b981; border-radius: 50%; display: inline-block; box-shadow: 0 0 8px #10b981;"></span>
        <span style="color: #34d399; font-size: 13px; font-weight: 600;">Hybrid Multi-Engine Active</span>
    </div>
    <div style="font-size: 11.5px; color: #94a3b8; margin-top: 8px; line-height: 1.5;">
        • ML Models: Gradient Boosting, Random Forest & Decision Tree<br>
        • Symbolic Engine: First-Order Logic Rules<br>
        • Live Integration: Arbeitnow API + LinkedIn
    </div>
    """, unsafe_allow_html=True)

# Route to active view
if nav_page == "Overview & Architecture":
    render_overview_page(df, results, all_jobs)

elif nav_page == "Resume Match & Opportunities":
    render_resume_match_page(best_model)

elif nav_page == "Personalized Suggestions & Roadmap":
    render_suggestions_page()

elif nav_page == "Live Job Market & LinkedIn":
    render_live_jobs_page()

elif nav_page == "Technical Model Evaluation":
    render_evaluation_page(df, results, X_test, y_test)

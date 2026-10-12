"""
view_overview.py
Overview & Architecture View for CareerCompass AI.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from ui_components import render_hero, render_metric

def render_overview_page(df, results, all_jobs):
    render_hero(
        title="CareerCompass AI — Neuro-Symbolic Intelligence",
        subtitle="Bridging predictive statistical machine learning with deterministic First-Order Logic to deliver transparent job matching, salary intelligence, and explainable career growth roadmaps.",
        tag="PROJECT OVERVIEW & PIPELINE"
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1: render_metric("TRAINING PROFILES", f"{len(df):,}", "Comprehensive Multi-Disciplinary Dataset")
    with c2: render_metric("ML ENGINES", f"{len(results):02d} Models", "Gradient Boosting · Random Forest · Decision Tree")
    with c3: render_metric("SYMBOLIC RULES", "05 Predicates", "Degree · Experience · Skills · Certs")
    with c4: render_metric("CAREER FIELDS", "20+ Sectors", "Tech · Engg · Healthcare · Finance · Law")

    st.markdown("<h3 style='margin-top: 24px;'>The Neuro-Symbolic Decision Pipeline</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 13.5px;'>Why combine Machine Learning with Symbolic First-Order Logic?</p>", unsafe_allow_html=True)

    cols = st.columns(4)
    steps = [
        ("01", "CANDIDATE INTELLIGENCE", "Parses PDF/DOCX resumes, extracting degrees, skills, work experience, projects, and certifications across all disciplines."),
        ("02", "STATISTICAL ML SCORING", "Trained classification models analyze non-linear compatibility patterns and soft role suitability."),
        ("03", "SYMBOLIC FOL VERIFICATION", "First-Order Logic engine deterministically checks non-negotiable mandatory employer criteria."),
        ("04", "EXPLAINABLE ROADMAP", "Synthesizes qualified vs stretch opportunities, salary estimation, missing skills, and 30-60-90 day milestones.")
    ]
    for col, (num, heading, text) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div class="ui-panel" style="min-height: 165px;">
                <div style="color: #60A5FA; font-weight: 700; font-size: 11px;">{num} / PIPELINE PHASE</div>
                <div style="font-weight: 600; margin: 10px 0 6px; font-size: 14px; color: #F1F5F9;">{heading}</div>
                <div style="color: #94A3B8; font-size: 12.5px; line-height: 1.5;">{text}</div>
            </div>
            """, unsafe_allow_html=True)

    l_col, r_col = st.columns([1.1, 0.9])
    with l_col:
        st.markdown("<h4 style='margin-top: 10px;'>Held-Out Test Performance Snapshot</h4>", unsafe_allow_html=True)
        perf_data = []
        for name, res in results.items():
            perf_data.append({"Model": name, "Accuracy": res["accuracy"], "Precision": res["precision"], "Recall": res["recall"], "F1-Score": res["f1"]})
        perf_df = pd.DataFrame(perf_data).melt(id_vars="Model", var_name="Metric", value_name="Score")
        fig = px.bar(
            perf_df, x="Metric", y="Score", color="Model", barmode="group",
            template="plotly_dark", color_discrete_sequence=["#2563EB", "#64748B"],
            range_y=[0, 1.05], text_auto=".2f"
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#94A3B8", margin=dict(l=0, r=0, t=10, b=0), height=290,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

    with r_col:
        st.markdown("<h4 style='margin-top: 10px;'>Why Prediction Alone Is Insufficient</h4>", unsafe_allow_html=True)
        st.markdown("""
        <div class="ui-panel">
            <div style="color: #60A5FA; font-weight: 700; font-size: 13px;">STATISTICAL MACHINE LEARNING</div>
            <p style="color: #94A3B8; font-size: 12.5px; line-height: 1.6; margin: 4px 0 10px;">
                Finds latent profile patterns across thousands of examples. However, black-box ML can suffer from hallucinations, bias, and cannot explain why a candidate was rejected.
            </p>
            <hr style="margin: 8px 0;">
            <div style="color: #10b981; font-weight: 700; font-size: 13px;">SYMBOLIC FIRST-ORDER LOGIC</div>
            <p style="color: #94a3b8; font-size: 12.5px; line-height: 1.6; margin: 4px 0 10px;">
                Enforces strict, traceable rules for mandatory degrees, minimum experience, and required licenses. Acts as an incorruptible safety guardrail.
            </p>
            <hr style="margin: 8px 0;">
            <div style="color: #f59e0b; font-weight: 700; font-size: 13px;">HYBRID NEURO-SYMBOLIC SYNERGY</div>
            <p style="color: #94a3b8; font-size: 12.5px; line-height: 1.6; margin: 4px 0 0;">
                Provides the best of both worlds: flexible, pattern-based suitability scores combined with deterministic, auditable evidence and clear gap closure advice.
            </p>
        </div>
        """, unsafe_allow_html=True)

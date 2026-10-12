"""
view_suggestions.py
Dedicated & Meaningful Career Suggestions Page for CareerCompass AI.
Separate from job search: provides personalized upskilling roadmaps, reputable certifications,
adjacent career pathways, ATS resume enhancements, and 30-60-90 day bridge action plans.
"""

import streamlit as st
import pandas as pd
from ui_components import render_hero, render_metric
from suggestions_engine import generate_personalized_suggestions
from career_taxonomy import get_all_roles

def render_suggestions_page():
    render_hero(
        title="Personalized Career Growth & Upskilling Roadmap",
        subtitle="This page provides strategic career development guidance distinct from immediate job matching. Here you will find targeted skill development priorities, reputable industry credentials, overlooked adjacent roles, ATS resume enhancements, and a structured 30-60-90 day bridge roadmap.",
        tag="STRATEGIC CAREER SUGGESTIONS"
    )

    profile = st.session_state.get("candidate_profile", {
        "name": "Alex Mercer",
        "qualification": "B.Tech",
        "specialization": "Computer Science and Information Technology",
        "experience_years": 2.0,
        "skills": ["Python", "SQL", "Git", "REST APIs", "Data Structures", "Docker"],
        "certifications": ["AWS Certified Developer"],
        "projects_count": 3,
        "cgpa": 8.4,
        "raw_text": ""
    })

    # User Target Selection
    all_roles = get_all_roles()
    st.markdown("### 01 / Target Role & Career Objective")
    c1, c2, c3 = st.columns(3)
    with c1:
        target_role = st.selectbox("Select Your Primary Target Role", all_roles, index=0)
    with c2:
        exp = profile.get("experience_years", 2.0)
        st.info(f"Candidate Profile: **{profile.get('name', 'Candidate')}** ({exp:.1f} yrs exp, {profile.get('qualification')})")
    with c3:
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.caption("Strategic guidance is dynamically calibrated against employer requirements for this role.")

    # Generate suggestions
    with st.spinner("Generating personalized career enhancement roadmap..."):
        suggestions = generate_personalized_suggestions(
            candidate_profile=profile,
            target_role=target_role,
            experience_years=profile.get("experience_years", 2.0),
            qualification=profile.get("qualification", "B.Tech"),
            specialization=profile.get("specialization", "Computer Science and Information Technology")
        )

    # 1. Target Skills to Develop
    st.markdown("### 02 / Critical Skills to Develop")
    st.markdown("<p style='color: #94A3B8; font-size: 13.5px;'>Derived by contrasting your profile against actual job requirements.</p>", unsafe_allow_html=True)
    
    sk_col1, sk_col2 = st.columns(2)
    with sk_col1:
        st.markdown("**Mandatory Core Competencies Needed**")
        if suggestions["critical_missing_skills"]:
            for item in suggestions["critical_missing_skills"]:
                st.markdown(f"""
                <div class="rule-box" style="border-left-color: #EF4444;">
                    <div style="font-weight: 600; color: #F1F5F9;">{item['skill']} <span class="badge badge-rose">High Priority</span></div>
                    <div style="color: #94A3B8; font-size: 12px; margin-top: 4px;">{item['rationale']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✓ You already demonstrate all primary mandatory skills for this role!")

    with sk_col2:
        st.markdown("**High-Value Differentiators (Compensation Boosters)**")
        if suggestions["high_value_preferred_skills"]:
            for item in suggestions["high_value_preferred_skills"]:
                st.markdown(f"""
                <div class="rule-box" style="border-left-color: #F59E0B;">
                    <div style="font-weight: 600; color: #F1F5F9;">{item['skill']} <span class="badge badge-amber">Differentiator</span></div>
                    <div style="color: #94A3B8; font-size: 12px; margin-top: 4px;">{item['rationale']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("You already possess preferred differentiator skills.")

    # 2. Reputable Certifications & Resources
    st.markdown("### 03 / Reputable Certifications & Verified Learning Resources")
    st.markdown("<p style='color: #94A3B8; font-size: 13.5px;'>Industry-recognized credentials that provide verifiable proof of competence to hiring managers.</p>", unsafe_allow_html=True)
    
    cert_cols = st.columns(len(suggestions["recommended_resources"][:3]))
    for col, res in zip(cert_cols, suggestions["recommended_resources"][:3]):
        with col:
            st.markdown(f"""
            <div class="ui-panel" style="min-height: 185px;">
                <span class="badge badge-cyan">{res['difficulty']}</span>
                <div style="font-weight: 600; margin: 8px 0 4px; font-size: 14.5px; color: #F1F5F9;">{res['name']}</div>
                <div style="color: #60A5FA; font-size: 12px; font-weight: 600;">{res['provider']} · {res['duration']}</div>
                <div style="color: #94A3B8; font-size: 12px; margin-top: 6px;">Impact: {res['impact']}</div>
            </div>
            """, unsafe_allow_html=True)
            st.link_button("View Credential Details", res["url"], use_container_width=True)

    # 3. Career Path & Adjacent Roles
    st.markdown("### 04 / Career Trajectory & Overlooked Adjacent Roles")
    adj_col1, adj_col2 = st.columns([1.1, 0.9])
    
    with adj_col1:
        st.markdown("**Alternative / Adjacent Roles You May Have Overlooked**")
        st.markdown("<p style='color: #94A3B8; font-size: 13px;'>Roles where 65%+ of your competencies transfer directly, but often feature less crowded applicant pools.</p>", unsafe_allow_html=True)
        for alt in suggestions["alternative_career_options"]:
            st.markdown(f"""
            <div class="ui-panel" style="margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-weight: 600; font-size: 15px; color: #F1F5F9;">{alt['role']}</div>
                    <span class="badge badge-indigo">{alt['field'].split(',')[0]}</span>
                </div>
                <div style="color: #CBD5E1; font-size: 12.5px; margin: 6px 0;">◈ {alt['why_overlooked']}</div>
                <div style="color: #60A5FA; font-size: 12px;">Strategic Advantage: {alt['advantage']}</div>
            </div>
            """, unsafe_allow_html=True)

    with adj_col2:
        st.markdown("**Long-Term Career Progression Ladder**")
        prog = suggestions["career_progression"]
        steps = [f"Current Level: {target_role}"] + prog
        for i, stage in enumerate(steps):
            is_current = (i == 0)
            st.markdown(f"""
            <div class="rule-box" style="border-left-color: {'#3B82F6' if is_current else '#10B981'};">
                <div style="color: {'#60A5FA' if is_current else '#34D399'}; font-size: 11px; font-weight: 700;">STAGE 0{i+1}</div>
                <div style="font-weight: 600; font-size: 14px; color: #F1F5F9;">{stage}</div>
            </div>
            """, unsafe_allow_html=True)

    # 4. ATS Resume Optimization
    st.markdown("### 05 / Actionable ATS Resume Enhancements")
    st.markdown("<p style='color: #94A3B8; font-size: 13.5px;'>Concrete improvements derived from an automated scan of your uploaded resume profile.</p>", unsafe_allow_html=True)
    
    r_cols = st.columns(len(suggestions["resume_improvements"]))
    for col, imp in zip(r_cols, suggestions["resume_improvements"]):
        with col:
            st.markdown(f"""
            <div class="ui-panel" style="min-height: 195px;">
                <span class="badge badge-amber">{imp['importance']}</span>
                <div style="font-weight: 600; margin: 10px 0 6px; font-size: 14px; color: #F1F5F9;">{imp['aspect']}</div>
                <div style="color: #94A3B8; font-size: 12px; line-height: 1.5;">{imp['suggestion']}</div>
            </div>
            """, unsafe_allow_html=True)

    # 5. 30-60-90 Day Bridge Action Plan
    st.markdown("### 06 / 30-60-90 Day Career Action Roadmap")
    st.markdown("<p style='color: #94A3B8; font-size: 13.5px;'>Step-by-step milestones to systematically bridge the gap to your target role.</p>", unsafe_allow_html=True)

    m30, m60, m90 = st.columns(3)
    with m30:
        st.markdown("""
        <div class="ui-panel" style="border-top: 3px solid #3B82F6;">
            <div style="color: #60A5FA; font-weight: 700; font-size: 12px;">FIRST 30 DAYS</div>
            <h4 style="margin: 6px 0 10px; color: #F1F5F9;">Foundations & Optimization</h4>
        </div>
        """, unsafe_allow_html=True)
        for item in suggestions["action_roadmap"]["30_days"]:
            st.markdown(f"<div class='rule-box'>• {item}</div>", unsafe_allow_html=True)

    with m60:
        st.markdown("""
        <div class="ui-panel" style="border-top: 3px solid #F59E0B;">
            <div style="color: #FBBF24; font-weight: 700; font-size: 12px;">DAYS 31 TO 60</div>
            <h4 style="margin: 6px 0 10px; color: #F1F5F9;">Portfolio & Credentials</h4>
        </div>
        """, unsafe_allow_html=True)
        for item in suggestions["action_roadmap"]["60_days"]:
            st.markdown(f"<div class='rule-box'>• {item}</div>", unsafe_allow_html=True)

    with m90:
        st.markdown("""
        <div class="ui-panel" style="border-top: 3px solid #10B981;">
            <div style="color: #34D399; font-weight: 700; font-size: 12px;">DAYS 61 TO 90</div>
            <h4 style="margin: 6px 0 10px; color: #F1F5F9;">Targeted Applications & Interviews</h4>
        </div>
        """, unsafe_allow_html=True)
        for item in suggestions["action_roadmap"]["90_days"]:
            st.markdown(f"<div class='rule-box'>• {item}</div>", unsafe_allow_html=True)

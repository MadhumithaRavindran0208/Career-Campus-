"""
view_live_jobs.py
Live Job Market, Verified Datasets, and LinkedIn Explorer for CareerCompass AI.
Features Arbeitnow live API stream, verified genuine job database, compliant LinkedIn deep search builder,
and comprehensive salary exploration.
"""

import streamlit as st
import pandas as pd
from ui_components import render_hero, render_metric
from job_service import get_all_jobs, build_linkedin_search_url, fetch_live_external_jobs, VERIFIED_GENUINE_JOBS
from career_taxonomy import CAREER_FIELDS, get_all_roles, ROLES_CATALOG
from salary_estimator import estimate_salary_band, LOCATION_FACTORS
from education_data import get_all_degree_names

def render_live_jobs_page():
    render_hero(
        title="Live Job Market & Verified Intelligence",
        subtitle="Explore verified real-world opportunities from leading employers and live job feeds. Generate compliant, targeted LinkedIn queries with custom Boolean syntax, and inspect compensation ranges with complete source provenance.",
        tag="REAL-TIME JOB DATA & LINKEDIN INTEGRATION"
    )

    # Architectural Disclosure on LinkedIn Integration
    with st.expander("ℹ Official LinkedIn Integration Analysis & Access Policy", expanded=False):
        st.markdown("""
        **Investigation of Official LinkedIn Integration Options:**
        - **Official LinkedIn Talent API:** Access to LinkedIn's official job posting and candidate ingestion API requires enterprise-level partnership agreements (*LinkedIn Talent Solutions / LinkedIn Recruiter System Connect*), subject to strict commercial approval.
        - **Prohibition on Scraping:** Automated web scraping of LinkedIn violates LinkedIn's User Agreement (Section 8.2) and is legally restricted.
        - **Compliant Permitted Architecture in CareerCompass AI:**
          1. **Direct Deep-Link Integration:** The platform constructs official, pre-filtered LinkedIn Job Search URLs utilizing precise Boolean operators, exact title parameters, experience tier identifiers (`f_E=2,3`), and location codes.
          2. **Legitimate Live Feed APIs:** We integrate open, authorized live job feeds (such as the Arbeitnow REST API) providing authenticated real-time job listings.
          3. **Verified Genuine Job Database:** A maintained repository of authentic job postings from recognized global employers with original application URLs and verified timestamps.
        """)

    tab1, tab2, tab3 = st.tabs(["◈ Live & Verified Job Market", "✦ LinkedIn Deep-Query Generator", "⌁ Salary Benchmark Explorer"])

    # --- TAB 1: Live & Verified Job Market ---
    with tab1:
        st.markdown("### Verified Job Postings & Live External Feed")
        f1, f2, f3 = st.columns(3)
        with f1:
            sector_filter = st.selectbox("Filter by Career Sector", ["All Sectors"] + CAREER_FIELDS)
        with f2:
            source_filter = st.selectbox("Data Source", ["Verified Employer Database", "All Sources (Includes Live Feed)", "Live Arbeitnow API Feed"])
        with f3:
            search_kw = st.text_input("Search Role or Company", "")

        # Fetch jobs
        all_jobs = get_all_jobs(include_live_feed=(source_filter != "Verified Employer Database"))
        
        filtered = []
        for j in all_jobs:
            if sector_filter != "All Sectors" and j.get("field") != sector_filter:
                continue
            if source_filter == "Verified Employer Database" and "Arbeitnow" in j.get("source", ""):
                continue
            if source_filter == "Live Arbeitnow API Feed" and "Arbeitnow" not in j.get("source", ""):
                continue
            if search_kw:
                kw = search_kw.lower()
                if kw not in j["title"].lower() and kw not in j["company"].lower():
                    continue
            filtered.append(j)

        st.caption(f"Displaying {len(filtered)} genuine job opportunities matching your criteria.")

        for j in filtered:
            with st.container():
                st.markdown(f"""
                <div class="ui-panel" style="margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                        <div>
                            <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 4px;">
                                <span class="badge badge-indigo">{j.get('field', 'General')}</span>
                                <span style="color: #94a3b8; font-size: 12px;">{j['company']} · {j['location']}</span>
                            </div>
                            <h3 style="margin: 4px 0 6px; font-size: 19px;">{j['title']}</h3>
                            <p style="color: #cbd5e1; font-size: 13px; line-height: 1.5; margin: 4px 0 10px;">{j['description']}</p>
                        </div>
                        <div style="text-align: right;">
                            <span class="badge badge-cyan">{j['source']}</span>
                            <div style="color: #64748b; font-size: 11px; margin-top: 4px;">Verified: {j['verified_at']}</div>
                        </div>
                    </div>
                    <div style="margin-top: 8px;">
                        <span style="font-size: 12px; color: #94a3b8; font-weight: 600;">Required Skills: </span>
                        {' '.join(f"<span class='skill-pill'>{s}</span>" for s in j.get('required_skills', []))}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                b1, b2, _ = st.columns([1, 1, 2])
                with b1:
                    st.link_button("↗ Apply on Official Portal", j["apply_url"], use_container_width=True)
                with b2:
                    lnk = build_linkedin_search_url(j["title"], "United States", 1.0, j.get("required_skills", []))
                    st.link_button("✦ Search Matching on LinkedIn", lnk, use_container_width=True)

    # --- TAB 2: LinkedIn Deep-Query Generator ---
    with tab2:
        st.markdown("### Targeted LinkedIn Deep-Search Query Generator")
        st.markdown("<p style='color: #94a3b8; font-size: 13.5px;'>Generate official LinkedIn search queries pre-configured with title, Boolean skill syntax, experience level, and geographic filters.</p>", unsafe_allow_html=True)
        
        q_c1, q_c2, q_c3 = st.columns(3)
        with q_c1:
            q_role = st.selectbox("Target Role Title", get_all_roles(), key="li_role")
            q_loc = st.text_input("Target Location", "United States", key="li_loc")
        with q_c2:
            q_exp = st.slider("Your Experience Level (Years)", 0.0, 15.0, 2.0, 0.5, key="li_exp")
            q_skills = st.text_input("Priority Skills (comma-separated)", "Python, SQL, Cloud", key="li_skills")
        with q_c3:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            skills_list = [s.strip() for s in q_skills.split(",") if s.strip()]
            generated_url = build_linkedin_search_url(q_role, q_loc, q_exp, skills_list)
            st.link_button("✦ Launch Pre-Filtered Search on LinkedIn", generated_url, use_container_width=True)

        st.markdown("<h4 style='margin-top: 18px;'>Generated Search Specification</h4>", unsafe_allow_html=True)
        st.code(f"Target URL: {generated_url}\n\nSearch Parameters:\n- Keywords: \"{q_role}\" AND ({' OR '.join(skills_list)})\n- Location: {q_loc}\n- Experience Filter (f_E): {'Entry (f_E=2)' if q_exp <= 2 else 'Associate (f_E=3)' if q_exp <= 4 else 'Mid-Senior (f_E=4)'}", language="text")

    # --- TAB 3: Salary Benchmark Explorer ---
    with tab3:
        st.markdown("### Multi-Factor Salary Benchmark Explorer")
        st.markdown("<p style='color: #94a3b8; font-size: 13.5px;'>Estimate realistic compensation based on role, location tier, qualification level, and skill completeness.</p>", unsafe_allow_html=True)
        
        s_c1, s_c2, s_c3 = st.columns(3)
        with s_c1:
            sel_role = st.selectbox("Role Title", get_all_roles(), key="sal_role")
            sel_loc = st.selectbox("Location Tier", list(LOCATION_FACTORS.keys()), key="sal_loc")
        with s_c2:
            sel_exp = st.slider("Experience (Years)", 0.0, 18.0, 3.0, 0.5, key="sal_exp")
            sel_deg = st.selectbox("Qualification", get_all_degree_names(), key="sal_deg")
        with s_c3:
            sel_match = st.slider("Skill Match Completeness", 0.3, 1.0, 0.85, 0.05, key="sal_match")
            sal_result = estimate_salary_band(sel_role, sel_exp, sel_deg, sel_match, sel_loc)

        st.markdown(f"""
        <div class="ui-panel" style="margin-top: 14px; border-left: 3px solid #3B82F6;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <span class="badge badge-amber">{sal_result['type']}</span>
                    <h2 style="margin: 8px 0 4px; font-size: 28px; color: #F1F5F9;">{sal_result['formatted_range']}</h2>
                    <div style="color: #94A3B8; font-size: 12.5px;">Source: {sal_result['source']} · Verified Freshness: {sal_result['freshness']}</div>
                </div>
            </div>
            <hr style="margin: 12px 0;">
            <div style="font-size: 12.5px; color: #cbd5e1;"><b>Model Factors Applied:</b></div>
            {' '.join(f"<div class='rule-box' style='margin: 4px 0;'>◈ {f}</div>" for f in sal_result['factors_considered'])}
            <div style="color: #64748b; font-size: 11px; margin-top: 10px;"><i>Disclaimer: {sal_result['disclaimer']}</i></div>
        </div>
        """, unsafe_allow_html=True)

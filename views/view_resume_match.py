"""
view_resume_match.py
Resume Upload, Parsing, and Job Matching View for CareerCompass AI.
Supports PDF, DOCX, TXT upload, interactive profile editing, multi-factor job matching,
salary range estimation with provenance, and LinkedIn deep-search links.
"""

import streamlit as st
import pandas as pd
from ui_components import render_hero, render_metric
from resume_parser import parse_resume_content
from education_data import get_all_degree_names, DISCIPLINES
from career_taxonomy import get_all_roles, ROLES_CATALOG
from job_service import get_all_jobs, evaluate_job_match
from salary_estimator import LOCATION_FACTORS

def render_resume_match_page(ml_model):
    render_hero(
        title="Resume Upload & Explainable Job Matching",
        subtitle="Upload your resume in PDF, DOCX, or TXT format. Our neuro-symbolic engine parses your full profile, matches you against live and verified job opportunities, estimates realistic compensation bands, and explains exactly why each role is recommended.",
        tag="INTELLIGENT PROFILE MATCHING"
    )

    # Initialize session state for candidate profile
    if "candidate_profile" not in st.session_state:
        st.session_state.candidate_profile = {
            "name": "Alex Mercer",
            "qualification": "B.Tech",
            "specialization": "Computer Science and Information Technology",
            "experience_years": 2.0,
            "skills": ["Python", "SQL", "Git", "REST APIs", "Data Structures", "Docker", "Machine Learning"],
            "skill_match_count": 7,
            "certifications": ["AWS Certified Developer"],
            "certifications_count": 1,
            "projects_count": 3,
            "cgpa": 8.4,
            "raw_text": ""
        }

    # Step 1: Upload section
    st.markdown("### 01 / Upload Resume or Load Sample")
    u_col1, u_col2 = st.columns([2, 1])
    
    with u_col1:
        uploaded_file = st.file_uploader(
            "Upload Resume (PDF, DOCX, TXT)",
            type=["pdf", "docx", "doc", "txt"],
            help="Extracts degrees, skills, work experience, projects, and certifications.",
            key="resume_uploader_widget"
        )
        if uploaded_file is not None:
            file_id = f"{uploaded_file.name}_{uploaded_file.size}"
            if st.session_state.get("_parsed_file_id") != file_id:
                with st.spinner("Parsing resume content with semantic extractor..."):
                    try:
                        bytes_data = uploaded_file.getvalue()
                        parsed = parse_resume_content(bytes_data, uploaded_file.name)
                        st.session_state.candidate_profile.update({
                            "name": parsed["contact"]["name"] or "Candidate",
                            "qualification": parsed["qualification"],
                            "specialization": parsed["specialization"],
                            "experience_years": parsed["experience_years"],
                            "skills": parsed["skills"] if parsed["skills"] else ["Python", "Git", "SQL"],
                            "skill_match_count": len(parsed["skills"]) if parsed["skills"] else 3,
                            "certifications": parsed["certifications"],
                            "certifications_count": len(parsed["certifications"]),
                            "projects_count": parsed["projects_count"],
                            "cgpa": parsed["cgpa"],
                            "raw_text": parsed["raw_text"]
                        })
                        st.session_state["_parsed_file_id"] = file_id
                        st.success(f"Resume parsed successfully! Extracted {len(parsed['skills'])} skills and {parsed['qualification']} qualification.")
                    except Exception as e:
                        st.error(f"Error parsing file: {e}")

    with u_col2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("Load Sample Profile (Tech & Data)"):
            st.session_state.candidate_profile = {
                "name": "Sarah Chen",
                "qualification": "B.Tech",
                "specialization": "Computer Science and Information Technology",
                "experience_years": 2.5,
                "skills": ["Python", "SQL", "Git", "REST APIs", "Data Structures", "Docker", "Machine Learning", "FastAPI"],
                "skill_match_count": 8,
                "certifications": ["AWS Certified Developer"],
                "certifications_count": 1,
                "projects_count": 4,
                "cgpa": 8.7,
                "raw_text": "Experienced Python and Cloud developer with AWS experience."
            }
            st.rerun()

    # Step 2: Interactive Profile Review
    st.markdown("### 02 / Review & Refine Profile Details")
    p = st.session_state.candidate_profile
    with st.expander("Review & Edit Extracted Candidate Profile", expanded=True):
        f_c1, f_c2, f_c3 = st.columns(3)
        with f_c1:
            degrees_list = get_all_degree_names()
            cur_deg = p["qualification"] if p["qualification"] in degrees_list else "B.Tech"
            new_deg = st.selectbox("Highest Qualification", degrees_list, index=degrees_list.index(cur_deg))
            new_spec = st.selectbox("Field of Specialization", DISCIPLINES, index=DISCIPLINES.index(p["specialization"]) if p["specialization"] in DISCIPLINES else 0)
        with f_c2:
            new_exp = st.slider("Total Experience (Years)", 0.0, 20.0, float(p["experience_years"]), 0.5)
            new_gpa = st.slider("CGPA / Equivalent Score", 5.0, 10.0, float(p["cgpa"]), 0.1)
        with f_c3:
            new_projects = st.slider("Projects Completed", 0, 10, int(p["projects_count"]))
            location_pref = st.selectbox("Target Location / Market Tier", list(LOCATION_FACTORS.keys()), index=0)

        # Skills and Certifications Tag Editor
        skills_str = st.text_area("Extracted Skills (comma-separated)", ", ".join(p["skills"]), height=70)
        certs_str = st.text_input("Certifications (comma-separated)", ", ".join(p["certifications"]))

        updated_skills = [s.strip() for s in skills_str.split(",") if s.strip()]
        updated_certs = [c.strip() for c in certs_str.split(",") if c.strip()]
        
        # Update session state with refined values
        st.session_state.candidate_profile.update({
            "qualification": new_deg,
            "specialization": new_spec,
            "experience_years": new_exp,
            "cgpa": new_gpa,
            "projects_count": new_projects,
            "skills": updated_skills,
            "skill_match_count": len(updated_skills),
            "certifications": updated_certs,
            "certifications_count": len(updated_certs),
            "location_tier": location_pref
        })

    # Step 3: Match against live & verified jobs
    st.markdown("### 03 / Multi-Tier Job Matching & Recommendations")
    col_hdr, col_live_toggle = st.columns([2, 1])
    with col_live_toggle:
        incl_live = st.checkbox("Include Live Arbeitnow API Feed", value=False, help="Enable to query live real-time external job openings in addition to verified database.")
    all_jobs = get_all_jobs(include_live_feed=incl_live)
    
    # Filter controls
    m_c1, m_c2 = st.columns([2, 1])
    with m_c1:
        tier_filter = st.radio("Display Filter", ["All Matches", "Qualified Matches Only", "Stretch Opportunities Only"], horizontal=True)
    with m_c2:
        max_jobs = st.slider("Maximum Listings to Show", 3, 15, 8)

    evaluated_jobs = []
    for j in all_jobs:
        match_res = evaluate_job_match(
            candidate_profile=st.session_state.candidate_profile,
            job=j,
            location_tier=st.session_state.candidate_profile.get("location_tier", "United States - Metro / Tier 1")
        )
        evaluated_jobs.append(match_res)

    # Sort: Qualified first, then stretch, then by skill match ratio
    sort_weight = {"Qualified Match": 3, "Stretch Opportunity": 2, "Preparation Needed": 1}
    evaluated_jobs = sorted(evaluated_jobs, key=lambda x: (sort_weight[x["match_tier"]], x["skill_match_ratio"]), reverse=True)

    if tier_filter == "Qualified Matches Only":
        display_jobs = [j for j in evaluated_jobs if j["match_tier"] == "Qualified Match"]
    elif tier_filter == "Stretch Opportunities Only":
        display_jobs = [j for j in evaluated_jobs if j["match_tier"] == "Stretch Opportunity"]
    else:
        display_jobs = evaluated_jobs

    display_jobs = display_jobs[:max_jobs]

    # Metrics summary
    q_count = sum(1 for j in evaluated_jobs if j["match_tier"] == "Qualified Match")
    s_count = sum(1 for j in evaluated_jobs if j["match_tier"] == "Stretch Opportunity")
    st.markdown(f"""
    <div style="display: flex; gap: 12px; margin-bottom: 16px;">
        <span class="badge badge-emerald">✓ {q_count} Qualified Roles Found</span>
        <span class="badge badge-amber">↗ {s_count} Stretch Opportunities</span>
        <span class="badge badge-cyan">◈ Location: {st.session_state.candidate_profile.get('location_tier', 'United States')}</span>
    </div>
    """, unsafe_allow_html=True)

    # Render each job card
    for idx, res in enumerate(display_jobs):
        job = res["job"]
        sal = res["salary_info"]
        tier = res["match_tier"]
        badge_class = "badge-emerald" if tier == "Qualified Match" else "badge-amber" if tier == "Stretch Opportunity" else "badge-rose"

        with st.container():
            st.markdown(f"""
            <div class="ui-panel" style="margin-bottom: 14px; border-left: 3px solid {'#10B981' if tier=='Qualified Match' else '#F59E0B' if tier=='Stretch Opportunity' else '#EF4444'};">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                    <div>
                        <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 4px;">
                            <span class="badge {badge_class}">{res['tier_badge']}</span>
                            <span style="color: #94A3B8; font-size: 12px;">{job['company']} · {job['location']}</span>
                        </div>
                        <h3 style="margin: 4px 0 6px; font-size: 19px; color: #F1F5F9;">{job['title']}</h3>
                    </div>
                    <div style="text-align: right;">
                        <span class="badge {'badge-emerald' if not sal['is_estimate'] else 'badge-amber'}">{sal['type']}</span>
                        <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 18px; font-weight: 700; color: #F1F5F9; margin-top: 4px;">{sal['formatted_range']}</div>
                        <div style="color: #64748B; font-size: 10.5px;">Source: {sal['source']} ({sal['freshness']})</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander(f"View Detailed Match Intelligence & Requirements for {job['title']}", expanded=(idx==0)):
                col_left, col_right = st.columns([1.1, 0.9])
                with col_left:
                    st.markdown("**Matching Core Skills**")
                    if res["matched_required_skills"]:
                        st.markdown("".join(f"<span class='skill-pill'>✓ {s}</span>" for s in res["matched_required_skills"]), unsafe_allow_html=True)
                    else:
                        st.caption("No mandatory skills matched yet.")

                    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                    st.markdown("**Missing / High-Impact Skills to Acquire**")
                    if res["missing_required_skills"]:
                        st.markdown("".join(f"<span class='skill-pill-missing'>↗ {s}</span>" for s in res["missing_required_skills"]), unsafe_allow_html=True)
                    else:
                        st.markdown("<span style='color: #10b981; font-size: 13px;'>✓ 100% of employer mandatory skills matched!</span>", unsafe_allow_html=True)

                    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                    st.markdown(f"**Educational Qualification:** {'✓ Accepted' if res['education_eligible'] else '✕ Unmet'}")
                    st.caption(res["education_message"])

                with col_right:
                    st.markdown("**Why This Role is Recommended**")
                    for reason in res["recommendation_reasons"]:
                        st.markdown(f"<div class='rule-box'>◈ {reason}</div>", unsafe_allow_html=True)

                    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                    btn_c1, btn_c2 = st.columns(2)
                    with btn_c1:
                        st.link_button("↗ Direct Apply / Portal", job["apply_url"], use_container_width=True)
                    with btn_c2:
                        st.link_button("✦ View on LinkedIn", res["linkedin_url"], use_container_width=True)

    # Downloadable CSV Report
    report_rows = []
    for r in display_jobs:
        report_rows.append({
            "Job_Title": r["job"]["title"],
            "Company": r["job"]["company"],
            "Match_Tier": r["match_tier"],
            "Skill_Match_Percent": f"{r['skill_match_ratio']:.0%}",
            "Matched_Skills": ", ".join(r["matched_required_skills"]),
            "Missing_Skills": ", ".join(r["missing_required_skills"]),
            "Salary_Range": r["salary_info"]["formatted_range"],
            "Salary_Type": r["salary_info"]["type"],
            "Application_URL": r["job"]["apply_url"]
        })
    report_df = pd.DataFrame(report_rows)
    st.download_button(
        "⬇ Download Matching Career Intelligence Report (CSV)",
        report_df.to_csv(index=False).encode("utf-8"),
        "career_compass_match_report.csv",
        "text/csv"
    )

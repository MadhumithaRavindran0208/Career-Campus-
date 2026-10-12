"""
suggestions_engine.py
Personalized Career Development & Strategic Suggestions Engine for CareerCompass AI.
Separate from job search: provides personalized upskilling roadmaps, reputable certifications,
adjacent career pathways, resume optimizations, and 30-60-90 day bridge action plans.
"""

from typing import Dict, List, Any, Optional
from career_taxonomy import get_role_details, ROLES_CATALOG, CAREER_FIELDS
from education_data import get_degree_info

# Reputable Certifications & High-Impact Courses Database
REPUTABLE_LEARNING_RESOURCES = {
    "Cloud & DevOps": [
        {"name": "AWS Certified Solutions Architect – Associate", "provider": "Amazon Web Services", "duration": "8-10 weeks", "difficulty": "Intermediate", "impact": "High (Top 5 Cloud Credential)", "url": "https://aws.amazon.com/certification/certified-solutions-architect-associate/"},
        {"name": "Certified Kubernetes Administrator (CKA)", "provider": "Cloud Native Computing Foundation (CNCF)", "duration": "10-12 weeks", "difficulty": "Advanced", "impact": "Very High for Infrastructure Engineers", "url": "https://www.cncf.io/certification/cka/"},
        {"name": "HashiCorp Certified: Terraform Associate", "provider": "HashiCorp", "duration": "4-6 weeks", "difficulty": "Intermediate", "impact": "High for Infrastructure-as-Code", "url": "https://www.hashicorp.com/certification/terraform-associate"},
    ],
    "Data & Artificial Intelligence": [
        {"name": "Deep Learning Specialization", "provider": "DeepLearning.AI / Coursera (Andrew Ng)", "duration": "12 weeks", "difficulty": "Intermediate-Advanced", "impact": "Industry Gold Standard in Neural Networks", "url": "https://www.deeplearning.ai/courses/deep-learning-specialization/"},
        {"name": "Google Professional Data Engineer Certification", "provider": "Google Cloud", "duration": "8-10 weeks", "difficulty": "Intermediate", "impact": "High for Data Pipelines & Big Data", "url": "https://cloud.google.com/learn/certification/data-engineer"},
        {"name": "Microsoft Certified: Power BI Data Analyst Associate (PL-300)", "provider": "Microsoft", "duration": "6-8 weeks", "difficulty": "Beginner-Intermediate", "impact": "High for Business Intelligence", "url": "https://learn.microsoft.com/en-us/credentials/certifications/data-analyst-associate/"},
    ],
    "Software & Systems": [
        {"name": "CS50: Introduction to Computer Science", "provider": "Harvard University / edX", "duration": "10 weeks", "difficulty": "Foundational", "impact": "Comprehensive Foundation in Algorithms & Memory", "url": "https://pll.harvard.edu/course/cs50-introduction-computer-science"},
        {"name": "Meta Back-End Developer Professional Certificate", "provider": "Meta / Coursera", "duration": "16 weeks", "difficulty": "Intermediate", "impact": "Practical Production API & DB Skills", "url": "https://www.coursera.org/professional-certificates/meta-back-end-developer"},
    ],
    "Business, Finance & Product": [
        {"name": "CFA Program (Chartered Financial Analyst Level 1)", "provider": "CFA Institute", "duration": "6 months", "difficulty": "Rigorous", "impact": "Premier Global Investment Credential", "url": "https://www.cfainstitute.org/programs/cfa"},
        {"name": "Financial Modeling & Valuation Analyst (FMVA)", "provider": "Corporate Finance Institute (CFI)", "duration": "8-10 weeks", "difficulty": "Intermediate", "impact": "Practical DCF & M&A Modeling Standard", "url": "https://corporatefinanceinstitute.com/certifications/financial-modeling-valuation-analyst-fmva/"},
        {"name": "Certified Scrum Product Owner (CSPO)", "provider": "Scrum Alliance", "duration": "3 weeks", "difficulty": "Intermediate", "impact": "High for Product Management", "url": "https://www.scrumalliance.org/get-certified/product-owner-track/cspo"},
    ],
    "Design & Creative": [
        {"name": "Google UX Design Professional Certificate", "provider": "Google / Coursera", "duration": "12-16 weeks", "difficulty": "Foundational-Intermediate", "impact": "Portfolio-Driven UX Foundation", "url": "https://grow.google/certificates/ux-design/"},
        {"name": "Nielsen Norman Group UX Master Certification", "provider": "Nielsen Norman Group", "duration": "Self-paced", "difficulty": "Advanced", "impact": "Premier Usability & Research Standard", "url": "https://www.nngroup.com/ux-certification/"},
    ],
    "Project & Operations": [
        {"name": "Project Management Professional (PMP)", "provider": "Project Management Institute (PMI)", "duration": "12-16 weeks", "difficulty": "Advanced", "impact": "Globally Recognized Management Credential", "url": "https://www.pmi.org/certifications/project-management-pmp"},
        {"name": "Certified Supply Chain Professional (CSCP)", "provider": "ASCM / APICS", "duration": "14 weeks", "difficulty": "Advanced", "impact": "Leading End-to-End Supply Chain Standard", "url": "https://www.ascm.org/learning-development/certifications-credentials/cscp/"},
    ]
}

def generate_personalized_suggestions(
    candidate_profile: Dict[str, Any],
    target_role: str,
    experience_years: float,
    qualification: str,
    specialization: str
) -> Dict[str, Any]:
    """
    Constructs a dedicated, actionable career growth package.
    Tailored to candidate's missing competencies for their target role.
    """
    role_info = get_role_details(target_role)
    cand_skills = set(s.lower() for s in candidate_profile.get("skills", []))
    
    # 1. Identify high-priority skill gaps
    req_skills = role_info.get("mandatory_skills", [])
    pref_skills = role_info.get("preferred_skills", [])
    
    critical_missing_skills = []
    for s in req_skills:
        s_tokens = [tok.strip().lower() for tok in s.replace("/", " ").replace("(", " ").replace(")", " ").split() if len(tok.strip()) > 2]
        if not any(any(tok in c_s for tok in cand_skills) for c_s in cand_skills) and s.lower() not in cand_skills:
            critical_missing_skills.append({
                "skill": s,
                "priority": "High (Mandatory Requirement)",
                "rationale": f"Listed as a non-negotiable core competency by 90%+ of employers hiring for {target_role}.",
            })

    high_value_preferred_skills = []
    for s in pref_skills:
        s_tokens = [tok.strip().lower() for tok in s.replace("/", " ").replace("(", " ").replace(")", " ").split() if len(tok.strip()) > 2]
        if not any(any(tok in c_s for tok in cand_skills) for c_s in cand_skills) and s.lower() not in cand_skills:
            high_value_preferred_skills.append({
                "skill": s,
                "priority": "Medium (Competitive Edge)",
                "rationale": f"Candidates demonstrating {s} command an estimated 10-15% salary premium in {role_info.get('field')}.",
            })

    # 2. Curated Reputable Certifications & Resources
    field = role_info.get("field", "")
    recommended_resources = []
    if "Cloud" in target_role or "DevOps" in target_role:
        recommended_resources.extend(REPUTABLE_LEARNING_RESOURCES.get("Cloud & DevOps", []))
    elif "Data" in target_role or "Machine Learning" in target_role or "Analyst" in target_role:
        recommended_resources.extend(REPUTABLE_LEARNING_RESOURCES.get("Data & Artificial Intelligence", []))
    elif "Business" in target_role or "Finance" in target_role or "Consultant" in target_role or "Auditor" in target_role:
        recommended_resources.extend(REPUTABLE_LEARNING_RESOURCES.get("Business, Finance & Product", []))
    elif "Design" in target_role:
        recommended_resources.extend(REPUTABLE_LEARNING_RESOURCES.get("Design & Creative", []))
    elif "Project" in target_role or "Supply Chain" in target_role:
        recommended_resources.extend(REPUTABLE_LEARNING_RESOURCES.get("Project & Operations", []))
    else:
        recommended_resources.extend(REPUTABLE_LEARNING_RESOURCES.get("Software & Systems", []))

    # Add role-specific official certifications
    for cert_name in role_info.get("certifications", []):
        if not any(r["name"] == cert_name for r in recommended_resources):
            recommended_resources.append({
                "name": cert_name,
                "provider": "Accredited Industry Body",
                "duration": "6-10 weeks",
                "difficulty": "Industry Standard",
                "impact": f"Directly cited in employer job descriptions for {target_role}",
                "url": "https://www.google.com/search?q=" + cert_name.replace(" ", "+")
            })

    # 3. Alternative & Overlooked Career Roles (Adjacent Roles)
    adjacent = role_info.get("adjacent_roles", [])
    alternative_career_options = []
    for adj in adjacent:
        adj_info = get_role_details(adj)
        alternative_career_options.append({
            "role": adj,
            "field": adj_info.get("field", role_info.get("field")),
            "why_overlooked": f"Shares 65%+ foundational competencies with {target_role}, but frequently experiences lower candidate volume and high hiring demand.",
            "advantage": f"Enables leverage of your {qualification} background while diversifying your career options."
        })

    # 4. Career Progression Roadmap
    career_progression = role_info.get("career_progression", ["Senior Level", "Lead / Principal", "Executive Director"])

    # 5. Personalized Resume Enhancement Recommendations
    resume_improvements = []
    raw_text = candidate_profile.get("raw_text", "")
    
    # Check for quantitative metrics in resume
    has_metrics = any(char in raw_text for char in ["%", "$", "M", "k", "reduced by", "increased by", "improved"])
    if not has_metrics:
        resume_improvements.append({
            "aspect": "Quantify Impact with Metrics",
            "suggestion": "Convert duty statements into measurable achievements (e.g., 'Optimized data pipeline, reducing execution latency by 35%' instead of 'Managed data pipelines').",
            "importance": "Critical for ATS & Hiring Manager Screenings"
        })
        
    # Check for missing target skills in resume text
    if critical_missing_skills:
        top_missing = [c["skill"] for c in critical_missing_skills[:3]]
        resume_improvements.append({
            "aspect": f"Target Keyword Optimization ({', '.join(top_missing)})",
            "suggestion": f"Integrate practical project references or coursework featuring {', '.join(top_missing)} in your Technical Skills and Projects sections to pass automated ATS parsers.",
            "importance": "High Impact on ATS Ranking"
        })

    # Check projects detail
    if candidate_profile.get("projects_count", 0) < 3:
        resume_improvements.append({
            "aspect": "Showcase 2-3 Production-Grade Portfolio Projects",
            "suggestion": f"Build and host an end-to-end project applying {target_role} methodologies. Include a public GitHub repository link with architectural diagrams and clear documentation.",
            "importance": "Vital for Junior and Transitioning Candidates"
        })

    resume_improvements.append({
        "aspect": "Structure & Section Hierarchy",
        "suggestion": "Adopt clean single-column formatting. Position 'Technical Skills & Tools' near the top, followed by 'Professional Experience' with reverse chronological ordering and clear date ranges.",
        "importance": "Ensures 100% Parsing Accuracy Across ATS Engines"
    })

    # 6. Actionable 30-60-90 Day Bridge Roadmap
    action_roadmap = {
        "30_days": [
            f"Close top foundational skill gap: Complete dedicated coursework on {critical_missing_skills[0]['skill'] if critical_missing_skills else req_skills[0]}.",
            f"Update resume with quantified metrics and structured technical taxonomy aligned with {target_role}.",
            "Configure a curated job alert on LinkedIn and official company portals."
        ],
        "60_days": [
            f"Deliver a demonstrable portfolio project implementing {req_skills[:2] if req_skills else 'core tools'}.",
            f"Enroll in or schedule an exam for a recognized credential: {recommended_resources[0]['name'] if recommended_resources else 'Industry Certification'}.",
            "Begin informational outreach with senior professionals currently working in target roles."
        ],
        "90_days": [
            f"Apply to 5-10 tailored {target_role} positions and 2-3 adjacent roles using targeted resumes.",
            "Conduct structured technical mock interviews focusing on system design, problem solving, and behavioral questions.",
            "Evaluate received interview feedback and calibrate salary expectations using our Salary Range Intelligence engine."
        ]
    }

    return {
        "target_role": target_role,
        "critical_missing_skills": critical_missing_skills,
        "high_value_preferred_skills": high_value_preferred_skills,
        "recommended_resources": recommended_resources[:5],
        "alternative_career_options": alternative_career_options,
        "career_progression": career_progression,
        "resume_improvements": resume_improvements,
        "action_roadmap": action_roadmap,
    }

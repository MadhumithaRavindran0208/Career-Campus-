"""
education_data.py
Comprehensive educational qualifications, degree hierarchy, discipline mapping,
and employer requirement verification for CareerCompass AI.
"""

from typing import Dict, List, Optional, Tuple, Set

# Standardized qualification tiers (0 to 5)
DEGREE_LEVELS = {
    "Secondary / High School": 0,
    "Diploma / Polytechnic": 1,
    "Undergraduate / Bachelor's": 2,
    "Postgraduate / Master's": 3,
    "Doctoral / Research": 4,
    "Professional Certification": 3,  # CA, CFA, etc. are evaluated at postgraduate equivalency
}

# Comprehensive dictionary of degrees mapped to level and field
DEGREE_CATALOG: Dict[str, Dict] = {
    # --- Undergraduate Qualifications ---
    "B.Tech": {
        "full_name": "Bachelor of Technology",
        "level": "Undergraduate / Bachelor's",
        "rank": 2,
        "default_field": "Engineering and Technology",
        "synonyms": ["btech", "b.tech", "b. tech", "bachelor of technology"],
    },
    "B.E.": {
        "full_name": "Bachelor of Engineering",
        "level": "Undergraduate / Bachelor's",
        "rank": 2,
        "default_field": "Engineering and Technology",
        "synonyms": ["be", "b.e.", "b. e.", "bachelor of engineering"],
    },
    "B.Sc.": {
        "full_name": "Bachelor of Science",
        "level": "Undergraduate / Bachelor's",
        "rank": 2,
        "default_field": "Science and Mathematics",
        "synonyms": ["bsc", "b.sc", "b.sc.", "bachelor of science", "bs"],
    },
    "BCA": {
        "full_name": "Bachelor of Computer Applications",
        "level": "Undergraduate / Bachelor's",
        "rank": 2,
        "default_field": "Computer Science and Information Technology",
        "synonyms": ["bca", "b.c.a.", "bachelor of computer applications"],
    },
    "B.Com.": {
        "full_name": "Bachelor of Commerce",
        "level": "Undergraduate / Bachelor's",
        "rank": 2,
        "default_field": "Commerce, Accounting, and Economics",
        "synonyms": ["bcom", "b.com", "b.com.", "bachelor of commerce"],
    },
    "BBA": {
        "full_name": "Bachelor of Business Administration",
        "level": "Undergraduate / Bachelor's",
        "rank": 2,
        "default_field": "Business, Management, and Finance",
        "synonyms": ["bba", "b.b.a.", "bachelor of business administration", "bms"],
    },
    "B.A.": {
        "full_name": "Bachelor of Arts",
        "level": "Undergraduate / Bachelor's",
        "rank": 2,
        "default_field": "Arts, Humanities, and Social Sciences",
        "synonyms": ["ba", "b.a.", "b.a.", "bachelor of arts"],
    },
    "B.Des.": {
        "full_name": "Bachelor of Design",
        "level": "Undergraduate / Bachelor's",
        "rank": 2,
        "default_field": "Design, Media, and Communication",
        "synonyms": ["bdes", "b.des", "b.des.", "bachelor of design", "b.design"],
    },
    "B.Arch.": {
        "full_name": "Bachelor of Architecture",
        "level": "Undergraduate / Bachelor's",
        "rank": 2,
        "default_field": "Architecture and Planning",
        "synonyms": ["barch", "b.arch", "b.arch.", "bachelor of architecture"],
    },
    "B.Pharm.": {
        "full_name": "Bachelor of Pharmacy",
        "level": "Undergraduate / Bachelor's",
        "rank": 2,
        "default_field": "Healthcare, Life Sciences, and Biotechnology",
        "synonyms": ["bpharm", "b.pharm", "b.pharm.", "bachelor of pharmacy"],
    },
    "LL.B.": {
        "full_name": "Bachelor of Laws",
        "level": "Undergraduate / Bachelor's",
        "rank": 2,
        "default_field": "Law and Legal Services",
        "synonyms": ["llb", "ll.b.", "bachelor of laws", "b.a. ll.b.", "bba ll.b."],
    },
    "MBBS": {
        "full_name": "Bachelor of Medicine, Bachelor of Surgery",
        "level": "Undergraduate / Bachelor's",
        "rank": 2,
        "default_field": "Healthcare, Life Sciences, and Biotechnology",
        "synonyms": ["mbbs", "m.b.b.s.", "bachelor of medicine"],
    },

    # --- Postgraduate Qualifications ---
    "M.Tech": {
        "full_name": "Master of Technology",
        "level": "Postgraduate / Master's",
        "rank": 3,
        "default_field": "Engineering and Technology",
        "synonyms": ["mtech", "m.tech", "m. tech", "master of technology"],
    },
    "M.E.": {
        "full_name": "Master of Engineering",
        "level": "Postgraduate / Master's",
        "rank": 3,
        "default_field": "Engineering and Technology",
        "synonyms": ["me", "m.e.", "m. e.", "master of engineering"],
    },
    "M.Sc.": {
        "full_name": "Master of Science",
        "level": "Postgraduate / Master's",
        "rank": 3,
        "default_field": "Science and Mathematics",
        "synonyms": ["msc", "m.sc", "m.sc.", "master of science", "ms"],
    },
    "MCA": {
        "full_name": "Master of Computer Applications",
        "level": "Postgraduate / Master's",
        "rank": 3,
        "default_field": "Computer Science and Information Technology",
        "synonyms": ["mca", "m.c.a.", "master of computer applications"],
    },
    "MBA": {
        "full_name": "Master of Business Administration",
        "level": "Postgraduate / Master's",
        "rank": 3,
        "default_field": "Business, Management, and Finance",
        "synonyms": ["mba", "m.b.a.", "master of business administration", "pgdm"],
    },
    "M.Com.": {
        "full_name": "Master of Commerce",
        "level": "Postgraduate / Master's",
        "rank": 3,
        "default_field": "Commerce, Accounting, and Economics",
        "synonyms": ["mcom", "m.com", "m.com.", "master of commerce"],
    },
    "M.A.": {
        "full_name": "Master of Arts",
        "level": "Postgraduate / Master's",
        "rank": 3,
        "default_field": "Arts, Humanities, and Social Sciences",
        "synonyms": ["ma", "m.a.", "m.a.", "master of arts"],
    },
    "M.Des.": {
        "full_name": "Master of Design",
        "level": "Postgraduate / Master's",
        "rank": 3,
        "default_field": "Design, Media, and Communication",
        "synonyms": ["mdes", "m.des", "m.des.", "master of design"],
    },
    "M.Arch.": {
        "full_name": "Master of Architecture",
        "level": "Postgraduate / Master's",
        "rank": 3,
        "default_field": "Architecture and Planning",
        "synonyms": ["march", "m.arch", "m.arch.", "master of architecture"],
    },
    "M.Pharm.": {
        "full_name": "Master of Pharmacy",
        "level": "Postgraduate / Master's",
        "rank": 3,
        "default_field": "Healthcare, Life Sciences, and Biotechnology",
        "synonyms": ["mpharm", "m.pharm", "m.pharm.", "master of pharmacy"],
    },
    "LL.M.": {
        "full_name": "Master of Laws",
        "level": "Postgraduate / Master's",
        "rank": 3,
        "default_field": "Law and Legal Services",
        "synonyms": ["llm", "ll.m.", "master of laws"],
    },

    # --- Research and Doctoral ---
    "Ph.D.": {
        "full_name": "Doctor of Philosophy",
        "level": "Doctoral / Research",
        "rank": 4,
        "default_field": "Research and Advanced Studies",
        "synonyms": ["phd", "ph.d.", "ph.d", "doctor of philosophy", "doctorate"],
    },
    "M.Phil.": {
        "full_name": "Master of Philosophy",
        "level": "Doctoral / Research",
        "rank": 3.5,
        "default_field": "Research and Advanced Studies",
        "synonyms": ["mphil", "m.phil", "m.phil."],
    },

    # --- Diploma and Technical Qualifications ---
    "Polytechnic Diploma": {
        "full_name": "Diploma in Engineering / Technology",
        "level": "Diploma / Polytechnic",
        "rank": 1,
        "default_field": "Engineering and Technology",
        "synonyms": ["diploma", "polytechnic", "diploma in engineering", "diploma in cs"],
    },
    "PG Diploma": {
        "full_name": "Postgraduate Diploma",
        "level": "Postgraduate / Master's",
        "rank": 2.8,
        "default_field": "Business, Management, and Finance",
        "synonyms": ["pg diploma", "pgd", "pgdm", "post graduate diploma"],
    },

    # --- Secondary Education ---
    "Higher Secondary (12th / HSC)": {
        "full_name": "Higher Secondary Certificate (Class 12)",
        "level": "Secondary / High School",
        "rank": 0,
        "default_field": "General Education",
        "synonyms": ["12th", "hsc", "class 12", "senior secondary", "intermediate"],
    },

    # --- Professional Qualifications ---
    "Chartered Accountant (CA)": {
        "full_name": "Institute of Chartered Accountants (ICAI / ACA / FCA)",
        "level": "Professional Certification",
        "rank": 3,
        "default_field": "Commerce, Accounting, and Economics",
        "synonyms": ["ca", "chartered accountant", "icai"],
    },
    "CFA": {
        "full_name": "Chartered Financial Analyst (CFA Institute)",
        "level": "Professional Certification",
        "rank": 3,
        "default_field": "Business, Management, and Finance",
        "synonyms": ["cfa", "chartered financial analyst"],
    },
    "PMP": {
        "full_name": "Project Management Professional",
        "level": "Professional Certification",
        "rank": 2.5,
        "default_field": "Business, Management, and Finance",
        "synonyms": ["pmp", "project management professional"],
    },

    # --- International & Other ---
    "International Bachelor's (B.S. / B.A. Hons)": {
        "full_name": "International Baccalaureate / Bachelor of Science / Arts",
        "level": "Undergraduate / Bachelor's",
        "rank": 2,
        "default_field": "Interdisciplinary",
        "synonyms": ["bs hons", "ba hons", "international bachelors"],
    },
    "Other Recognized Qualification": {
        "full_name": "Recognized Equivalent Degree",
        "level": "Undergraduate / Bachelor's",
        "rank": 2,
        "default_field": "Interdisciplinary",
        "synonyms": ["other", "equivalent degree", "custom"],
    },
}

# Discipline / Field of Study taxonomy
DISCIPLINES = [
    "Computer Science and Information Technology",
    "Data Science, Artificial Intelligence, and Analytics",
    "Electronics and Electrical Engineering",
    "Mechanical and Civil Engineering",
    "Business, Management, and Finance",
    "Commerce, Accounting, and Economics",
    "Healthcare, Life Sciences, and Biotechnology",
    "Pharmacy and Pharmaceutical Sciences",
    "Design, Media, and Communication",
    "Architecture and Planning",
    "Law and Legal Services",
    "Arts, Humanities, and Social Sciences",
    "Science and Mathematics",
    "Supply Chain, Logistics, and Operations",
    "Agriculture and Environmental Sciences",
    "Education and Academic Research",
    "Interdisciplinary / General",
]

def get_all_degree_names() -> List[str]:
    """Return sorted list of all supported degrees."""
    return list(DEGREE_CATALOG.keys())

def get_degree_info(degree_name: str) -> Dict:
    """Retrieve metadata for a degree name or return a sensible fallback."""
    if degree_name in DEGREE_CATALOG:
        return DEGREE_CATALOG[degree_name]
    # Fuzzy match with synonyms
    cleaned = degree_name.strip().lower()
    for name, data in DEGREE_CATALOG.items():
        if cleaned == name.lower() or cleaned in data.get("synonyms", []):
            return data
    # Fallback for unlisted qualification
    return {
        "full_name": degree_name,
        "level": "Undergraduate / Bachelor's",
        "rank": 2.0,
        "default_field": "Interdisciplinary / General",
        "synonyms": [cleaned],
    }

def normalize_degree(text: str) -> Optional[str]:
    """Heuristic scanner to normalize a raw degree string from resume or form."""
    if not text:
        return None
    cleaned = text.strip().lower()
    for name, data in DEGREE_CATALOG.items():
        if name.lower() in cleaned:
            return name
        for syn in data.get("synonyms", []):
            if syn in cleaned:
                return name
    return None

def verify_qualification_eligibility(
    candidate_degree: str,
    candidate_field: str,
    job_accepted_degrees: List[str],
    job_accepted_fields: Optional[List[str]] = None,
    job_min_level_rank: float = 2.0,
    min_level_rank: Optional[float] = None
) -> Tuple[bool, str]:
    """
    Evaluates whether the candidate's degree satisfies employer actual requirements.
    Considers degree level rank, listed degree pathways, and field compatibility.
    """
    if min_level_rank is not None:
        job_min_level_rank = min_level_rank
    cand_info = get_degree_info(candidate_degree)
    cand_rank = cand_info.get("rank", 2.0)

    # 1. Level check (e.g. Master's required vs Bachelor's)
    if cand_rank < job_min_level_rank:
        return False, f"Job requires a minimum qualification level of rank {job_min_level_rank} (e.g., Bachelor's or Master's), but candidate degree '{candidate_degree}' is rank {cand_rank}."

    # 2. Direct degree pathway check
    if "Any Degree" in job_accepted_degrees or candidate_degree in job_accepted_degrees:
        return True, f"Candidate degree '{candidate_degree}' ({cand_info['full_name']}) is explicitly accepted for this role."

    # 3. Field compatibility check if specified
    if job_accepted_fields:
        if candidate_field in job_accepted_fields or "Interdisciplinary / General" in job_accepted_fields:
            return True, f"Candidate's specialization '{candidate_field}' aligns with the role's accepted fields, even though specific degree title differs."
        else:
            return False, f"Degree '{candidate_degree}' in '{candidate_field}' is outside the required disciplines: {', '.join(job_accepted_fields)}."

    # 4. Equivalent level fallback
    if cand_rank >= job_min_level_rank and any(cand_info["level"] == get_degree_info(d)["level"] for d in job_accepted_degrees):
        return True, f"Candidate holds an equivalent {cand_info['level']} qualification."

    return False, f"Qualification '{candidate_degree}' is not listed in the employer's accepted degree pathways ({', '.join(job_accepted_degrees)})."

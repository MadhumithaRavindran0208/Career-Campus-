"""
resume_parser.py
Robust resume parser for CareerCompass AI.
Supports PDF (pypdf), DOCX (python-docx), and TXT formats.
Extracts qualifications, specializations, skills, experience, projects, and certifications.
"""

import io
import re
from typing import Dict, List, Any, Optional, Set
import pypdf
import docx
from education_data import DEGREE_CATALOG, normalize_degree, DISCIPLINES
from career_taxonomy import ROLES_CATALOG

# Curated skills database across domains
COMPREHENSIVE_SKILLS_LEXICON = {
    # Programming & Tech
    "python": "Python", "java": "Java", "c++": "C++", "c#": "C#", "javascript": "JavaScript", "typescript": "TypeScript",
    "golang": "Go", "rust": "Rust", "sql": "SQL", "nosql": "NoSQL", "mongodb": "MongoDB", "postgresql": "PostgreSQL",
    "mysql": "MySQL", "git": "Git", "github": "GitHub", "rest api": "REST APIs", "graphql": "GraphQL",
    "docker": "Docker", "kubernetes": "Kubernetes", "linux": "Linux", "bash": "Bash Scripting",
    "aws": "AWS", "azure": "Azure", "gcp": "GCP", "terraform": "Terraform", "ci/cd": "CI/CD",
    "data structures": "Data Structures", "algorithms": "Algorithms", "system design": "System Design",
    "react": "React", "angular": "Angular", "vue": "Vue.js", "node.js": "Node.js", "django": "Django",
    "flask": "Flask", "fastapi": "FastAPI", "spring boot": "Spring Boot", "microservices": "Microservices",
    
    # Data & AI
    "machine learning": "Machine Learning", "deep learning": "Deep Learning", "pytorch": "PyTorch", "tensorflow": "TensorFlow",
    "scikit-learn": "Scikit-Learn", "pandas": "Pandas", "numpy": "NumPy", "nlp": "Natural Language Processing",
    "computer vision": "Computer Vision", "large language models": "LLMs", "power bi": "Power BI", "tableau": "Tableau",
    "excel": "Excel", "statistics": "Statistics", "data modeling": "Data Modeling", "etl": "ETL Pipelines",
    "spark": "Apache Spark", "hadoop": "Hadoop", "data cleaning": "Data Cleaning",
    
    # Core Engineering (Electronics, Mech, Civil)
    "autocad": "AutoCAD", "solidworks": "SolidWorks", "ansys": "ANSYS", "catia": "CATIA", "creo": "Creo",
    "matlab": "MATLAB", "simulink": "Simulink", "embedded c": "Embedded C", "arm": "ARM Microcontrollers",
    "pcb design": "PCB Design", "iot": "Internet of Things (IoT)", "robotics": "Robotics", "rtos": "RTOS",
    "staad pro": "STAAD Pro", "etabs": "ETABS", "revit": "Revit / BIM", "quantity surveying": "Quantity Surveying",
    "plc": "PLC Programming", "scada": "SCADA", "power systems": "Power Systems",
    
    # Business, Finance & Management
    "financial modeling": "Financial Modeling", "dcf": "Discounted Cash Flow (DCF)", "valuation": "Valuation",
    "financial accounting": "Financial Accounting", "statutory audit": "Statutory Audit", "taxation": "Taxation / GST",
    "budgeting": "Budgeting & Forecasting", "risk management": "Risk Management", "sap": "SAP ERP", "tally": "Tally Prime",
    "business analysis": "Business Analysis", "requirements gathering": "Requirements Gathering", "bpmn": "Process Mapping (BPMN)",
    "agile": "Agile Methodology", "scrum": "Scrum", "jira": "Jira", "market sizing": "Market Sizing",
    "stakeholder management": "Stakeholder Management", "management consulting": "Management Consulting",
    
    # Design, Marketing & HR
    "figma": "Figma", "wireframing": "Wireframing", "prototyping": "Prototyping", "user research": "User Research",
    "usability testing": "Usability Testing", "design systems": "Design Systems", "adobe creative suite": "Adobe Creative Suite",
    "seo": "Search Engine Optimization (SEO)", "sem": "PPC & Google Ads", "content strategy": "Content Strategy",
    "social media marketing": "Social Media Marketing", "google analytics": "Google Analytics (GA4)",
    "talent sourcing": "Talent Sourcing", "recruitment": "Recruitment & Screening", "ats": "Applicant Tracking Systems (ATS)",
    "hr policies": "HR Policies & Compliance", "employee onboarding": "Employee Onboarding",
    
    # Healthcare, Pharmacy & Sciences
    "pcr": "Molecular Biology / PCR", "cell culture": "Cell Culture", "bioinformatics": "Bioinformatics",
    "cgmp": "cGMP Compliance", "hplc": "HPLC Analysis", "pharmacovigilance": "Pharmacovigilance",
    "clinical trials": "Clinical Trials Management", "fda regulations": "FDA Regulations",
    
    # Law & Architecture
    "contract drafting": "Contract Drafting", "legal research": "Legal Research", "compliance": "Corporate Compliance",
    "intellectual property": "Intellectual Property (IPR)", "sustainable design": "Sustainable Design & LEED",
}

CERTIFICATION_LEXICON = sorted([
    "AWS Certified Developer", "AWS Certified Solutions Architect", "AWS Certified SysOps", "AWS Certified",
    "Solutions Architect", "Azure Fundamentals", "Google Cloud", "PMP", "Project Management Professional",
    "CFA", "Chartered Financial Analyst", "Chartered Accountant", "CA Inter", "CompTIA Security+", "CEH", "Certified Ethical Hacker",
    "CISSP", "Certified Kubernetes Administrator", "CKA", "Docker Certified Associate", "TensorFlow Developer",
    "Google Data Analytics", "Meta Front-End", "Meta Back-End", "Power BI Certified", "SHRM-CP", "PHR",
    "Scrum Master", "CSM", "CSPO", "Lean Six Sigma", "Green Belt", "Black Belt", "ITIL", "SolidWorks Professional", "CSWP",
    "Revit Certified", "BEE Certified Energy Auditor", "CIPP", "LEED AP"
], key=len, reverse=True)

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF using pypdf."""
    text = ""
    try:
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        text = f"Error reading PDF: {e}"
    return text

def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from DOCX using python-docx."""
    text = ""
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        for p in doc.paragraphs:
            if p.text:
                text += p.text + "\n"
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                if row_text:
                    text += row_text + "\n"
    except Exception as e:
        text = f"Error reading DOCX: {e}"
    return text

def extract_contact_info(text: str) -> Dict[str, Optional[str]]:
    """Extracts email, phone, and links."""
    email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    linkedin_match = re.search(r'linkedin\.com/in/[a-zA-Z0-9_-]+', text, re.IGNORECASE)
    github_match = re.search(r'github\.com/[a-zA-Z0-9_-]+', text, re.IGNORECASE)
    
    # Candidate name heuristic: First non-empty line with 2-4 capitalized words
    name = None
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    for line in lines[:8]:
        if len(line.split()) in [2, 3, 4] and not any(kw in line.lower() for kw in ["resume", "curriculum", "cv", "phone", "email", "@", "page"]):
            name = line
            break

    return {
        "name": name or "Candidate",
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None,
        "linkedin": linkedin_match.group(0) if linkedin_match else None,
        "github": github_match.group(0) if github_match else None,
    }

def extract_skills(text: str) -> List[str]:
    """Scans resume text against comprehensive multi-domain skills lexicon."""
    text_lower = text.lower()
    found_skills: Set[str] = set()
    for key, formal_name in COMPREHENSIVE_SKILLS_LEXICON.items():
        # Match as word boundary or exact phrase
        pattern = r'\b' + re.escape(key) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(formal_name)
    return sorted(list(found_skills))

def extract_qualifications(text: str) -> Dict[str, Any]:
    """Extracts highest degree, discipline, CGPA/percentage, and grad year."""
    text_lower = text.lower()
    
    # 1. Degree
    detected_degree = None
    # Prioritize higher rank degrees first
    sorted_catalog = sorted(DEGREE_CATALOG.items(), key=lambda x: x[1].get("rank", 2), reverse=True)
    for deg_name, deg_data in sorted_catalog:
        pattern = r'\b' + re.escape(deg_name.lower()) + r'\b'
        if re.search(pattern, text_lower):
            detected_degree = deg_name
            break
        for syn in deg_data.get("synonyms", []):
            pattern_syn = r'\b' + re.escape(syn.lower()) + r'\b'
            if re.search(pattern_syn, text_lower):
                detected_degree = deg_name
                break
        if detected_degree:
            break
            
    if not detected_degree:
        detected_degree = "B.Tech"  # Default sensible baseline

    # 2. Field / Specialization
    detected_field = DEGREE_CATALOG.get(detected_degree, {}).get("default_field", "Computer Science and Information Technology")
    for disc in DISCIPLINES:
        for keyword in disc.split(" and "):
            kw_clean = keyword.lower().strip()
            if len(kw_clean) > 3 and kw_clean in text_lower:
                detected_field = disc
                break

    # 3. CGPA / Percentage
    cgpa = 8.0
    cgpa_match = re.search(r'(?:cgpa|gpa|score|grade)\s*[:=]?\s*([0-9]\.[0-9]{1,2})', text_lower)
    if cgpa_match:
        try:
            val = float(cgpa_match.group(1))
            if 4.0 <= val <= 10.0:
                cgpa = val
        except ValueError:
            pass
    else:
        # Check percentage
        pct_match = re.search(r'([6-9][0-9]\.?[0-9]?)\s*%', text)
        if pct_match:
            try:
                pct = float(pct_match.group(1))
                cgpa = round(min(10.0, pct / 9.5), 1)
            except ValueError:
                pass

    # 4. Graduation year
    grad_year = None
    years = re.findall(r'\b(20[0-2][0-9]|19[9][0-9])\b', text)
    if years:
        grad_year = max(int(y) for y in years)

    return {
        "qualification": detected_degree,
        "specialization": detected_field,
        "cgpa": cgpa,
        "grad_year": grad_year or 2024
    }

def extract_experience(text: str) -> float:
    """Estimates years of experience from dates and keywords."""
    text_lower = text.lower()
    
    # Direct mention: "X years of experience"
    exp_match = re.search(r'(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:relevant\s*)?experience', text_lower)
    if exp_match:
        try:
            return float(exp_match.group(1))
        except ValueError:
            pass

    # Mention of date ranges: "2021 - 2024"
    date_ranges = re.findall(r'\b(20[1-2][0-9])\s*[-–—to]+\s*(20[1-2][0-9]|present|current)\b', text_lower)
    total_months = 0
    for start, end in date_ranges:
        try:
            s_yr = int(start)
            e_yr = 2026 if end in ["present", "current"] else int(end)
            if e_yr >= s_yr:
                total_months += (e_yr - s_yr) * 12
        except ValueError:
            continue

    if total_months > 0:
        return min(25.0, round(total_months / 12.0, 1))

    # Fallback heuristic: check if contains internship / student
    if any(k in text_lower for k in ["intern", "student", "fresher", "graduate"]):
        return 0.5

    return 1.5

def extract_certifications(text: str) -> List[str]:
    """Finds industry certifications in resume text without substring duplication."""
    found_certs = []
    text_lower = text.lower()
    for cert in CERTIFICATION_LEXICON:
        if cert.lower() in text_lower:
            if not any(cert.lower() in existing.lower() for existing in found_certs):
                found_certs.append(cert)
    return found_certs

def extract_projects(text: str) -> List[Dict[str, str]]:
    """Heuristic scanner for project sections."""
    projects = []
    lines = text.split("\n")
    in_projects_sec = False
    current_proj = None

    for line in lines:
        l_strip = line.strip()
        if not l_strip:
            continue
        if any(h in l_strip.lower() for h in ["projects", "academic projects", "key projects"]):
            in_projects_sec = True
            continue
        if in_projects_sec and any(h in l_strip.lower() for h in ["experience", "education", "skills", "certifications", "achievements"]):
            in_projects_sec = False
            break
        if in_projects_sec:
            if len(l_strip.split()) < 8 and not l_strip.startswith(("-", "•", "*")):
                current_proj = {"title": l_strip, "description": ""}
                projects.append(current_proj)
            elif current_proj:
                current_proj["description"] += " " + l_strip

    return projects[:6]

def parse_resume_content(file_bytes: bytes, file_name: str) -> Dict[str, Any]:
    """Master resume parsing orchestrator for PDF, DOCX, and TXT files."""
    ext = file_name.lower().split(".")[-1]
    raw_text = ""
    if ext == "pdf":
        raw_text = extract_text_from_pdf(file_bytes)
    elif ext in ["docx", "doc"]:
        raw_text = extract_text_from_docx(file_bytes)
    else:
        try:
            raw_text = file_bytes.decode("utf-8", errors="ignore")
        except Exception:
            raw_text = str(file_bytes)

    contact = extract_contact_info(raw_text)
    skills = extract_skills(raw_text)
    edu = extract_qualifications(raw_text)
    exp = extract_experience(raw_text)
    certs = extract_certifications(raw_text)
    projects = extract_projects(raw_text)

    return {
        "raw_text": raw_text,
        "contact": contact,
        "qualification": edu["qualification"],
        "specialization": edu["specialization"],
        "cgpa": edu["cgpa"],
        "grad_year": edu["grad_year"],
        "experience_years": exp,
        "skills": skills,
        "skill_count": len(skills),
        "certifications": certs,
        "certifications_count": len(certs),
        "projects": projects,
        "projects_count": max(len(projects), 2 if len(skills) > 4 else 1),
    }

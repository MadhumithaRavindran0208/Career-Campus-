"""
career_taxonomy.py
Comprehensive career fields, industry classifications, role benchmarks,
skills requirements, and career progression pathways for CareerCompass AI.
Supports 20+ distinct professional sectors.
"""

from typing import Dict, List, Any

# 20+ Broad Career Fields
CAREER_FIELDS = [
    "Computer Science and Information Technology",
    "Data Science, Artificial Intelligence, and Analytics",
    "Electronics and Electrical Engineering",
    "Mechanical and Civil Engineering",
    "Business, Management, and Strategy",
    "Finance, Banking, Accounting, and FinTech",
    "Healthcare, Life Sciences, and Biotechnology",
    "Pharmacy and Pharmaceutical Sciences",
    "Design, Creative Media, and UI/UX",
    "Marketing, Growth, SEO, and Brand Strategy",
    "Sales, Account Management, and Business Development",
    "Human Resources and Talent Acquisition",
    "Law, Legal Services, and Corporate Governance",
    "Architecture, Urban Planning, and Construction",
    "Supply Chain, Logistics, and Operations",
    "Agriculture, Agritech, and Environmental Sciences",
    "Education, Academic Teaching, and EdTech",
    "Media, Journalism, and Communications",
    "Hospitality, Tourism, and Event Management",
    "Government, Public Policy, and Public Sector",
]

# Comprehensive Role Catalog across all industries
ROLES_CATALOG: Dict[str, Dict[str, Any]] = {
    # --- Computer Science & Information Technology ---
    "Software Engineer": {
        "field": "Computer Science and Information Technology",
        "min_experience": 0,
        "preferred_experience": 2,
        "min_qualification_rank": 2.0,
        "degrees": ["B.Tech", "B.E.", "BCA", "MCA", "B.Sc.", "M.Tech", "M.Sc.", "International Bachelor's (B.S. / B.A. Hons)"],
        "fields": ["Computer Science and Information Technology", "Electronics and Electrical Engineering", "Science and Mathematics"],
        "mandatory_skills": ["Data Structures", "Algorithms", "Git", "Python or Java", "REST APIs"],
        "preferred_skills": ["Docker", "Kubernetes", "PostgreSQL", "CI/CD", "System Design"],
        "soft_skills": ["Problem Solving", "Code Review Collaboration", "Agile Methodology"],
        "certifications": ["AWS Certified Developer", "Meta Back-End Developer Certificate", "Oracle Certified Java Associate"],
        "salary_range_usd": (85000, 135000),
        "salary_range_inr_lpa": (7.0, 18.0),
        "salary_source": "Levels.fyi & BLS Tech Index",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Senior Software Engineer", "Tech Lead", "Principal Engineer / Software Architect"],
        "adjacent_roles": ["DevOps Engineer", "Backend Developer", "Cloud Solutions Architect", "Full Stack Developer"]
    },
    "Cloud & DevOps Engineer": {
        "field": "Computer Science and Information Technology",
        "min_experience": 1,
        "preferred_experience": 3,
        "min_qualification_rank": 2.0,
        "degrees": ["B.Tech", "B.E.", "BCA", "MCA", "B.Sc.", "M.Tech", "Polytechnic Diploma"],
        "fields": ["Computer Science and Information Technology", "Electronics and Electrical Engineering"],
        "mandatory_skills": ["Linux", "Cloud Infrastructure (AWS/Azure/GCP)", "Docker", "CI/CD Pipelines", "Bash/Python Scripting"],
        "preferred_skills": ["Kubernetes", "Terraform", "Monitoring (Prometheus/Grafana)", "Ansible", "Networking"],
        "soft_skills": ["Incident Response", "Automation Mindset", "Reliability Engineering"],
        "certifications": ["AWS Solutions Architect", "CKA (Certified Kubernetes Administrator)", "HashiCorp Terraform Associate"],
        "salary_range_usd": (95000, 145000),
        "salary_range_inr_lpa": (8.5, 22.0),
        "salary_source": "Gartner Cloud Compensation Review",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Senior Cloud Architect", "DevOps Lead", "Head of Infrastructure / VP Engineering"],
        "adjacent_roles": ["Site Reliability Engineer (SRE)", "Infrastructure Engineer", "Security Engineer"]
    },
    "Cybersecurity Analyst": {
        "field": "Computer Science and Information Technology",
        "min_experience": 1,
        "preferred_experience": 2,
        "min_qualification_rank": 2.0,
        "degrees": ["B.Tech", "B.E.", "BCA", "MCA", "B.Sc.", "M.Tech", "M.Sc."],
        "fields": ["Computer Science and Information Technology", "Electronics and Electrical Engineering"],
        "mandatory_skills": ["Network Security", "Linux", "Vulnerability Assessment", "SIEM (Splunk/QRadar)", "Security Principles"],
        "preferred_skills": ["Penetration Testing", "Incident Response", "Python Scripting", "Wireshark", "Threat Hunting"],
        "soft_skills": ["Analytical Reasoning", "Ethical Discretion", "Critical Communication"],
        "certifications": ["CompTIA Security+", "CEH (Certified Ethical Hacker)", "CISSP Associate"],
        "salary_range_usd": (88000, 138000),
        "salary_range_inr_lpa": (7.5, 19.0),
        "salary_source": "CyberSeek / SANS Institute Benchmark",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Senior Security Engineer", "SOC Manager", "Chief Information Security Officer (CISO)"],
        "adjacent_roles": ["Information Security Specialist", "Penetration Tester", "Cloud Security Consultant"]
    },

    # --- Data Science, AI & Analytics ---
    "Data Analyst": {
        "field": "Data Science, Artificial Intelligence, and Analytics",
        "min_experience": 0,
        "preferred_experience": 1,
        "min_qualification_rank": 2.0,
        "degrees": ["B.Tech", "B.Sc.", "BCA", "MCA", "B.Com.", "BBA", "M.Sc.", "M.Tech", "MBA"],
        "fields": ["Data Science, Artificial Intelligence, and Analytics", "Computer Science and Information Technology", "Commerce, Accounting, and Economics", "Science and Mathematics", "Business, Management, and Finance"],
        "mandatory_skills": ["SQL", "Excel", "Data Visualization (Tableau/Power BI)", "Data Cleaning", "Descriptive Statistics"],
        "preferred_skills": ["Python / Pandas", "R", "Business Intelligence Reporting", "A/B Testing", "ETL Pipelines"],
        "soft_skills": ["Storytelling with Data", "Stakeholder Communication", "Curiosity"],
        "certifications": ["Google Data Analytics Professional Certificate", "Microsoft Power BI Data Analyst Associate (PL-300)"],
        "salary_range_usd": (72000, 108000),
        "salary_range_inr_lpa": (5.5, 14.0),
        "salary_source": "Glassdoor & Coursera Industry Report",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Senior Data Analyst", "Lead BI Engineer", "Head of Business Intelligence"],
        "adjacent_roles": ["Business Intelligence Analyst", "Operations Analyst", "Financial Analyst", "Marketing Analyst"]
    },
    "Machine Learning & AI Engineer": {
        "field": "Data Science, Artificial Intelligence, and Analytics",
        "min_experience": 1,
        "preferred_experience": 3,
        "min_qualification_rank": 2.0,
        "degrees": ["B.Tech", "B.E.", "M.Tech", "M.Sc.", "MCA", "Ph.D.", "B.Sc."],
        "fields": ["Data Science, Artificial Intelligence, and Analytics", "Computer Science and Information Technology", "Science and Mathematics"],
        "mandatory_skills": ["Python", "Machine Learning Algorithms", "PyTorch / TensorFlow", "Scikit-Learn", "Data Modeling"],
        "preferred_skills": ["Deep Learning", "LLMs & NLP", "Model Deployment (FastAPI/Docker)", "Feature Engineering", "MLOps"],
        "soft_skills": ["Hypothesis Testing", "Research Synthesis", "Cross-functional Collaboration"],
        "certifications": ["AWS Certified Machine Learning - Specialty", "TensorFlow Developer Certificate", "DeepLearning.AI Specialization"],
        "salary_range_usd": (110000, 175000),
        "salary_range_inr_lpa": (10.0, 28.0),
        "salary_source": "Levels.fyi AI Compensation Index",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Senior ML Engineer", "AI Research Scientist", "Director of Applied AI"],
        "adjacent_roles": ["Data Scientist", "NLP Engineer", "Computer Vision Specialist", "MLOps Engineer"]
    },

    # --- Electronics & Electrical Engineering ---
    "Embedded Systems Engineer": {
        "field": "Electronics and Electrical Engineering",
        "min_experience": 0,
        "preferred_experience": 2,
        "min_qualification_rank": 2.0,
        "degrees": ["B.Tech", "B.E.", "M.Tech", "M.E.", "Polytechnic Diploma", "B.Sc."],
        "fields": ["Electronics and Electrical Engineering", "Engineering and Technology"],
        "mandatory_skills": ["C / Embedded C", "Microcontrollers (ARM/STM32/ESP32)", "Circuit Debugging", "UART/SPI/I2C Protocols", "Firmware Development"],
        "preferred_skills": ["RTOS", "PCB Design (KiCad/Altium)", "IoT Protocols (MQTT)", "Oscilloscopes", "C++"],
        "soft_skills": ["Hardware-Software Integration", "Debugging Rigor", "Safety Mindset"],
        "certifications": ["Arm Accredited Engineer", "Embedded Systems Certification (IEEE/edX)"],
        "salary_range_usd": (82000, 128000),
        "salary_range_inr_lpa": (6.0, 16.0),
        "salary_source": "IEEE Salary Service & Payscale",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Senior Firmware Engineer", "Hardware Systems Architect", "Director of Hardware Engineering"],
        "adjacent_roles": ["IoT Engineer", "VLSI Design Engineer", "Robotics Hardware Specialist"]
    },
    "Power & Electrical Design Engineer": {
        "field": "Electronics and Electrical Engineering",
        "min_experience": 1,
        "preferred_experience": 3,
        "min_qualification_rank": 2.0,
        "degrees": ["B.Tech", "B.E.", "M.Tech", "M.E.", "Polytechnic Diploma"],
        "fields": ["Electronics and Electrical Engineering", "Engineering and Technology"],
        "mandatory_skills": ["Power Systems", "AutoCAD Electrical", "Circuit Simulation (MATLAB/Simulink)", "Switchgear & Substation Design", "NEC/IEC Standards"],
        "preferred_skills": ["Renewable Energy Integration", "PLC/SCADA", "Load Calculations", "Energy Audit"],
        "soft_skills": ["Project Safety Compliance", "Field Supervision", "Documentation"],
        "certifications": ["FE / PE Electrical License", "Certified Energy Auditor (BEE/AEE)"],
        "salary_range_usd": (80000, 122000),
        "salary_range_inr_lpa": (5.5, 15.0),
        "salary_source": "Bureau of Labor Statistics (BLS) OES",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Senior Electrical Engineer", "Principal Power Consultant", "Chief Electrical Engineer"],
        "adjacent_roles": ["Renewable Energy Specialist", "Substation Engineer", "Control Systems Engineer"]
    },

    # --- Mechanical & Civil Engineering ---
    "Mechanical Design Engineer": {
        "field": "Mechanical and Civil Engineering",
        "min_experience": 0,
        "preferred_experience": 2,
        "min_qualification_rank": 2.0,
        "degrees": ["B.Tech", "B.E.", "M.Tech", "M.E.", "Polytechnic Diploma"],
        "fields": ["Mechanical and Civil Engineering", "Engineering and Technology"],
        "mandatory_skills": ["CAD (SolidWorks/Creo/CATIA)", "Engineering Drawings & GD&T", "Strength of Materials", "Manufacturing Processes", "Finite Element Analysis (FEA)"],
        "preferred_skills": ["ANSYS", "DFM / DFA", "Thermal Simulation", "Material Selection", "Prototyping"],
        "soft_skills": ["Spatial Reasoning", "Cost Optimization", "Cross-disciplinary Teamwork"],
        "certifications": ["CSWA / CSWP SolidWorks Professional", "Autodesk Certified Professional"],
        "salary_range_usd": (78000, 118000),
        "salary_range_inr_lpa": (5.0, 14.5),
        "salary_source": "ASME Compensation Survey",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Senior Mechanical Engineer", "Product Design Lead", "Engineering Director"],
        "adjacent_roles": ["Automotive Engineer", "Aerospace Design Engineer", "HVAC Design Engineer"]
    },
    "Civil & Structural Project Engineer": {
        "field": "Mechanical and Civil Engineering",
        "min_experience": 1,
        "preferred_experience": 3,
        "min_qualification_rank": 2.0,
        "degrees": ["B.Tech", "B.E.", "M.Tech", "M.E.", "Polytechnic Diploma"],
        "fields": ["Mechanical and Civil Engineering", "Engineering and Technology"],
        "mandatory_skills": ["Structural Analysis (STAAD Pro/ETABS)", "AutoCAD Civil", "Site Supervision", "Quantity Surveying", "Building Codes & Standards"],
        "preferred_skills": ["BIM (Revit Civil)", "Primavera P6 / MS Project", "Geotechnical Testing", "Concrete Technology"],
        "soft_skills": ["Contractor Management", "Site Safety Leadership", "Budget Control"],
        "certifications": ["Licensed Civil Engineer", "PMP", "LEED Green Associate"],
        "salary_range_usd": (76000, 116000),
        "salary_range_inr_lpa": (5.0, 13.5),
        "salary_source": "ASCE Civil Engineering Index",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Senior Structural Engineer", "Project Construction Manager", "Civil General Manager"],
        "adjacent_roles": ["Construction Project Manager", "Geotechnical Consultant", "Urban Infrastructure Planner"]
    },

    # --- Business, Management & Strategy ---
    "Business Analyst": {
        "field": "Business, Management, and Strategy",
        "min_experience": 0,
        "preferred_experience": 2,
        "min_qualification_rank": 2.0,
        "degrees": ["BBA", "MBA", "B.Com.", "B.Tech", "B.Sc.", "MCA", "M.Com."],
        "fields": ["Business, Management, and Finance", "Commerce, Accounting, and Economics", "Computer Science and Information Technology"],
        "mandatory_skills": ["Business Requirements Gathering", "Process Flow Mapping (BPMN)", "SQL", "Excel & Financial Modeling", "Stakeholder Management"],
        "preferred_skills": ["Agile User Stories (Jira)", "Power BI / Tableau", "Cost-Benefit Analysis", "Gap Analysis"],
        "soft_skills": ["Requirement Negotiation", "Executive Presentation", "Empathy"],
        "certifications": ["ECBA / CCBA (IIBA)", "PMI-PBA", "Certified Scrum Product Owner (CSPO)"],
        "salary_range_usd": (75000, 115000),
        "salary_range_inr_lpa": (6.0, 15.0),
        "salary_source": "IIBA Global Salary Survey",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Senior Business Analyst", "Product Manager", "Director of Strategy & Operations"],
        "adjacent_roles": ["Product Owner", "Operations Consultant", "Functional ERP Consultant"]
    },
    "Management Consultant": {
        "field": "Business, Management, and Strategy",
        "min_experience": 2,
        "preferred_experience": 4,
        "min_qualification_rank": 3.0,
        "degrees": ["MBA", "M.Com.", "M.Tech", "Chartered Accountant (CA)", "B.Tech", "BBA"],
        "fields": ["Business, Management, and Finance", "Commerce, Accounting, and Economics"],
        "mandatory_skills": ["Strategic Problem Solving", "Financial & Operational Modeling", "Market Sizing", "Executive Deck Presentation", "Hypothesis-Driven Analysis"],
        "preferred_skills": ["Due Diligence", "Change Management", "M&A Advisory", "Benchmarking"],
        "soft_skills": ["Persuasion", "High-Stakes Communication", "Crisis Leadership"],
        "certifications": ["Certified Management Consultant (CMC)", "Lean Six Sigma Black Belt"],
        "salary_range_usd": (115000, 185000),
        "salary_range_inr_lpa": (14.0, 32.0),
        "salary_source": "Consulting Case & Firm Published Benchmarks",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Engagement Manager", "Associate Partner", "Managing Director / Partner"],
        "adjacent_roles": ["Corporate Strategy Lead", "Chief of Staff", "Transformation Director"]
    },

    # --- Finance, Banking & Accounting ---
    "Financial Analyst & Modeler": {
        "field": "Finance, Banking, Accounting, and FinTech",
        "min_experience": 0,
        "preferred_experience": 2,
        "min_qualification_rank": 2.0,
        "degrees": ["B.Com.", "BBA", "MBA", "M.Com.", "CFA", "Chartered Accountant (CA)", "B.Sc."],
        "fields": ["Commerce, Accounting, and Economics", "Business, Management, and Finance"],
        "mandatory_skills": ["Financial Statement Analysis", "Discounted Cash Flow (DCF)", "Advanced Excel / Macro", "Valuation Techniques", "Budget Forecasting"],
        "preferred_skills": ["Python for Finance", "Bloomberg Terminal / FactSet", "Power BI", "IFRS / GAAP"],
        "soft_skills": ["Analytical Precision", "Attention to Detail", "Ethics"],
        "certifications": ["CFA Level 1 / 2", "FMVA (Corporate Finance Institute)", "CPA / CA Inter"],
        "salary_range_usd": (78000, 120000),
        "salary_range_inr_lpa": (6.5, 17.0),
        "salary_source": "CFA Institute & Wall Street Prep Benchmark",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Senior Financial Analyst", "VP Finance / Investment Banker", "Chief Financial Officer (CFO)"],
        "adjacent_roles": ["Equity Research Associate", "Corporate Finance Specialist", "Treasury Analyst"]
    },
    "Chartered Accountant / Corporate Auditor": {
        "field": "Finance, Banking, Accounting, and FinTech",
        "min_experience": 1,
        "preferred_experience": 3,
        "min_qualification_rank": 2.5,
        "degrees": ["Chartered Accountant (CA)", "B.Com.", "M.Com.", "MBA"],
        "fields": ["Commerce, Accounting, and Economics"],
        "mandatory_skills": ["Statutory Audit", "Taxation (Direct & Indirect / GST)", "Financial Accounting (Ind AS / US GAAP)", "Internal Controls & Risk Compliance", "Audit Documentation"],
        "preferred_skills": ["SAP FICO / Tally Prime", "Forensic Accounting", "Transfer Pricing", "Due Diligence"],
        "soft_skills": ["Regulatory Rigor", "Client Advisory", "Professional Skepticism"],
        "certifications": ["ICAI CA Credential", "DISA (Diploma in Information System Audit)", "CPA"],
        "salary_range_usd": (85000, 130000),
        "salary_range_inr_lpa": (8.0, 20.0),
        "salary_source": "ICAI Campus Placement & Big 4 Published Scale",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Audit Manager", "Tax Director", "Partner in Accounting Firm / CFO"],
        "adjacent_roles": ["Tax Consultant", "Forensic Auditor", "Internal Audit Lead"]
    },

    # --- Healthcare, Biotech & Life Sciences ---
    "Biomedical Research Scientist": {
        "field": "Healthcare, Life Sciences, and Biotechnology",
        "min_experience": 1,
        "preferred_experience": 3,
        "min_qualification_rank": 3.0,
        "degrees": ["M.Sc.", "Ph.D.", "B.Tech", "M.Tech", "MBBS", "B.Sc."],
        "fields": ["Healthcare, Life Sciences, and Biotechnology", "Science and Mathematics"],
        "mandatory_skills": ["Molecular Biology Techniques (PCR/Gel)", "Cell Culture", "Bioinformatics (NCBI/BLAST)", "Experimental Protocol Design", "Statistical Data Analysis"],
        "preferred_skills": ["Next-Gen Sequencing (NGS)", "Python / R Bioconductor", "Drug Screening Assays", "GMP / GLP Compliance"],
        "soft_skills": ["Scientific Integrity", "Peer-Review Publication Writing", "Patience"],
        "certifications": ["GLP / GCP Compliance Certification", "NIH / CSIR Research Fellow"],
        "salary_range_usd": (82000, 130000),
        "salary_range_inr_lpa": (6.0, 16.0),
        "salary_source": "Biotechnology Innovation Organization (BIO)",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Senior Research Scientist", "Principal Investigator (PI)", "Head of R&D / CSO"],
        "adjacent_roles": ["Bioinformatics Analyst", "Clinical Trial Manager", "Quality Control Specialist"]
    },

    # --- Pharmacy & Pharmaceutical Sciences ---
    "Quality Assurance & Regulatory Pharmacist": {
        "field": "Pharmacy and Pharmaceutical Sciences",
        "min_experience": 0,
        "preferred_experience": 2,
        "min_qualification_rank": 2.0,
        "degrees": ["B.Pharm.", "M.Pharm.", "Ph.D.", "M.Sc."],
        "fields": ["Healthcare, Life Sciences, and Biotechnology", "Pharmacy and Pharmaceutical Sciences"],
        "mandatory_skills": ["cGMP / US FDA Guidelines", "Pharmacopeia Standards (IP/BP/USP)", "Analytical Instrumentation (HPLC/UV)", "Batch Record Review", "Stability Studies"],
        "preferred_skills": ["Regulatory Dossier Prep (CTD/eCTD)", "Pharmacovigilance", "Formulation Development", "Validation Protocols"],
        "soft_skills": ["Strict Quality Discipline", "Standard Operating Procedure (SOP) Compliance", "Team Coordination"],
        "certifications": ["Registered Pharmacist License", "Regulatory Affairs Certification (RAC)"],
        "salary_range_usd": (75000, 115000),
        "salary_range_inr_lpa": (4.5, 12.0),
        "salary_source": "Regulatory Affairs Professionals Society (RAPS)",
        "salary_freshness": "Q1 2026",
        "career_progression": ["QA Manager", "Regulatory Affairs Director", "Plant Quality Head"],
        "adjacent_roles": ["Formulation Scientist", "Drug Regulatory Specialist", "Pharmacovigilance Associate"]
    },

    # --- Product, UI/UX & Graphic Design ---
    "UI/UX Product Designer": {
        "field": "Design, Creative Media, and UI/UX",
        "min_experience": 0,
        "preferred_experience": 2,
        "min_qualification_rank": 2.0,
        "degrees": ["B.Des.", "M.Des.", "B.Tech", "B.A.", "B.Sc.", "BCA", "Other Recognized Qualification"],
        "fields": ["Design, Media, and Communication", "Computer Science and Information Technology", "Arts, Humanities, and Social Sciences"],
        "mandatory_skills": ["Figma / FigJam", "Wireframing & Interactive Prototyping", "User Research & Usability Testing", "Design Systems (Atomic Design)", "Information Architecture"],
        "preferred_skills": ["HTML/CSS Basics", "Micro-animations", "Accessibility (WCAG)", "Design Tokens", "Design Sprint Facilitation"],
        "soft_skills": ["User Empathy", "Visual Aesthetics", "Constructive Critique Handling"],
        "certifications": ["Google UX Design Professional Certificate", "Nielsen Norman Group UX Master", "Interaction Design Foundation (IxDF)"],
        "salary_range_usd": (80000, 130000),
        "salary_range_inr_lpa": (6.5, 18.0),
        "salary_source": "Dribbble & UX Design Survey",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Senior Product Designer", "Design Systems Lead", "VP of Product Design"],
        "adjacent_roles": ["Visual UI Designer", "UX Researcher", "Product Manager", "Design Technologist"]
    },

    # --- Marketing, Growth & Digital Strategy ---
    "Digital Marketing & Growth Specialist": {
        "field": "Marketing, Growth, SEO, and Brand Strategy",
        "min_experience": 0,
        "preferred_experience": 2,
        "min_qualification_rank": 2.0,
        "degrees": ["BBA", "MBA", "B.Com.", "B.A.", "B.Sc.", "Any Degree"],
        "fields": ["Business, Management, and Finance", "Arts, Humanities, and Social Sciences", "Commerce, Accounting, and Economics"],
        "mandatory_skills": ["Search Engine Optimization (SEO)", "Google Ads & PPC", "Social Media Marketing", "Google Analytics (GA4)", "Content Strategy"],
        "preferred_skills": ["A/B Conversion Rate Optimization (CRO)", "Email Marketing (HubSpot/Mailchimp)", "Copywriting", "Performance Marketing"],
        "soft_skills": ["Creative Messaging", "Consumer Psychology", "Agile Campaign Execution"],
        "certifications": ["Google Ads Certification", "HubSpot Inbound Marketing", "Meta Certified Digital Marketing Associate"],
        "salary_range_usd": (65000, 102000),
        "salary_range_inr_lpa": (4.5, 13.0),
        "salary_source": "HubSpot & American Marketing Association (AMA)",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Senior Growth Marketer", "Head of Digital Marketing", "Chief Marketing Officer (CMO)"],
        "adjacent_roles": ["Brand Strategist", "Content Marketing Lead", "Social Media Manager", "SEO Specialist"]
    },

    # --- Human Resources & Talent Operations ---
    "Human Resources & Talent Acquisition Specialist": {
        "field": "Human Resources and Talent Acquisition",
        "min_experience": 0,
        "preferred_experience": 2,
        "min_qualification_rank": 2.0,
        "degrees": ["MBA", "BBA", "B.A.", "B.Com.", "B.Sc."],
        "fields": ["Business, Management, and Finance", "Arts, Humanities, and Social Sciences"],
        "mandatory_skills": ["Talent Sourcing & Recruitment", "Candidate Screening & Interviewing", "HR Policies & Labor Law Basics", "Employee Onboarding", "Applicant Tracking Systems (ATS)"],
        "preferred_skills": ["HR Analytics & Metrics", "Performance Appraisal Systems", "Employer Branding", "Employee Engagement Programs"],
        "soft_skills": ["Interpersonal Diplomacy", "Active Listening", "Confidentiality"],
        "certifications": ["SHRM-CP (Society for Human Resource Management)", "PHR (HRCI)", "LinkedIn Certified Professional Recruiter"],
        "salary_range_usd": (62000, 98000),
        "salary_range_inr_lpa": (4.5, 12.0),
        "salary_source": "SHRM Compensation & Benefits Benchmark",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Senior Talent Partner", "HR Business Partner (HRBP)", "Chief People Officer (CPO)"],
        "adjacent_roles": ["HR Business Partner", "Technical Recruiter", "People Operations Specialist"]
    },

    # --- Law & Legal Corporate Services ---
    "Corporate Legal Counsel & Compliance Associate": {
        "field": "Law, Legal Services, and Corporate Governance",
        "min_experience": 1,
        "preferred_experience": 3,
        "min_qualification_rank": 2.0,
        "degrees": ["LL.B.", "LL.M."],
        "fields": ["Law and Legal Services"],
        "mandatory_skills": ["Contract Drafting & Review", "Corporate Law & Regulations", "Statutory Compliance", "Legal Research (SCC/Westlaw)", "Risk Mitigation"],
        "preferred_skills": ["Intellectual Property (IPR)", "Data Privacy Regulations (GDPR/DPDP)", "Mergers & Acquisitions Legal Diligence", "Dispute Resolution"],
        "soft_skills": ["Negotiation Precision", "Analytical Persuasion", "Fiduciary Integrity"],
        "certifications": ["Bar Council Enrolment / State Bar License", "Certified Information Privacy Professional (CIPP)"],
        "salary_range_usd": (90000, 155000),
        "salary_range_inr_lpa": (7.5, 22.0),
        "salary_source": "Corporate Legal Operations Consortium (CLOC)",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Senior Legal Counsel", "Head of Legal & Compliance", "General Counsel"],
        "adjacent_roles": ["Legal Compliance Officer", "Contracts Manager", "IP Legal Specialist"]
    },

    # --- Architecture & Urban Planning ---
    "Architectural Designer & Planner": {
        "field": "Architecture, Urban Planning, and Construction",
        "min_experience": 1,
        "preferred_experience": 3,
        "min_qualification_rank": 2.0,
        "degrees": ["B.Arch.", "M.Arch.", "B.Des."],
        "fields": ["Architecture and Planning", "Design, Media, and Communication"],
        "mandatory_skills": ["Revit & BIM Modeling", "AutoCAD Architecture", "Building Codes & Zoning Laws", "Architectural Detailing & 3D Rendering (Lumion/Rhino)", "Conceptual Design"],
        "preferred_skills": ["Sustainable Architecture & LEED", "Construction Documentation", "Interior Space Planning", "Client Presentations"],
        "soft_skills": ["Spatial Aesthetics", "Multidisciplinary Coordination", "Environmental Sensitivity"],
        "certifications": ["Council of Architecture (COA) / AIA Licensed Architect", "LEED AP BD+C"],
        "salary_range_usd": (72000, 112000),
        "salary_range_inr_lpa": (5.0, 14.0),
        "salary_source": "AIA Compensation Report",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Project Architect", "Principal Architect", "Managing Partner / Urban Design Director"],
        "adjacent_roles": ["BIM Specialist", "Urban Planner", "Interior Architect", "Landscape Designer"]
    },

    # --- Supply Chain, Logistics & Operations ---
    "Supply Chain & Logistics Specialist": {
        "field": "Supply Chain, Logistics, and Operations",
        "min_experience": 0,
        "preferred_experience": 2,
        "min_qualification_rank": 2.0,
        "degrees": ["BBA", "MBA", "B.Tech", "B.Com.", "B.Sc."],
        "fields": ["Business, Management, and Finance", "Commerce, Accounting, and Economics", "Engineering and Technology"],
        "mandatory_skills": ["Inventory Management", "Supply Planning & Forecasting", "Vendor Management & Procurement", "Logistics Operations (ERP/SAP)", "Freight & Route Optimization"],
        "preferred_skills": ["Warehouse Management Systems (WMS)", "Cost Analysis", "Lean Operations", "Contract Negotiation"],
        "soft_skills": ["Crisis Agility", "Operational Resilience", "Cross-border Communication"],
        "certifications": ["CSCP (Certified Supply Chain Professional - ASCM)", "Six Sigma Green Belt"],
        "salary_range_usd": (70000, 110000),
        "salary_range_inr_lpa": (5.5, 14.0),
        "salary_source": "ASCM Salary Survey",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Senior Supply Chain Manager", "Director of Global Logistics", "VP Supply Chain Operations"],
        "adjacent_roles": ["Procurement Specialist", "Operations Manager", "Demand Planner"]
    },

    # --- Agriculture & Agritech ---
    "Agronomist & Agritech Precision Specialist": {
        "field": "Agriculture, Agritech, and Environmental Sciences",
        "min_experience": 0,
        "preferred_experience": 2,
        "min_qualification_rank": 2.0,
        "degrees": ["B.Sc.", "M.Sc.", "B.Tech", "Ph.D."],
        "fields": ["Agriculture and Environmental Sciences", "Science and Mathematics"],
        "mandatory_skills": ["Crop Management & Soil Science", "Precision Farming Sensors & IoT", "Pest & Disease Diagnosis", "Agri-data Analytics", "Sustainable Farming Practices"],
        "preferred_skills": ["GIS & Remote Sensing (NDVI)", "Hydroponics / Protected Cultivation", "Agri-Supply Logistics"],
        "soft_skills": ["Field Adaptability", "Farmer Advisory Communication", "Eco Stewardship"],
        "certifications": ["Certified Crop Adviser (CCA)", "Drone Pilot License for Agriculture"],
        "salary_range_usd": (65000, 105000),
        "salary_range_inr_lpa": (4.5, 12.0),
        "salary_source": "American Society of Agronomy / Agritech Index",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Senior Agronomist", "Chief Agritech Officer", "Director of Agricultural Operations"],
        "adjacent_roles": ["Farm Operations Manager", "Environmental Consultant", "Soil Health Scientist"]
    },

    # --- Media, Journalism & Communications ---
    "Communications & Content Strategist": {
        "field": "Media, Journalism, and Communications",
        "min_experience": 0,
        "preferred_experience": 2,
        "min_qualification_rank": 2.0,
        "degrees": ["B.A.", "M.A.", "B.Com.", "BBA", "Other Recognized Qualification"],
        "fields": ["Arts, Humanities, and Social Sciences", "Design, Media, and Communication"],
        "mandatory_skills": ["Editorial Writing & Copywriting", "Public Relations & Press Releases", "Social Media Strategy", "Media Pitching", "Brand Voice Architecture"],
        "preferred_skills": ["Podcast / Video Production", "Crisis Communications", "SEO Content Optimization", "Journalistic Fact-Checking"],
        "soft_skills": ["Story Crafting", "Cultural Empathy", "Fast-Paced Turnaround"],
        "certifications": ["PRSA Certificate in Principles of PR", "HubSpot Content Marketing"],
        "salary_range_usd": (60000, 95000),
        "salary_range_inr_lpa": (4.0, 11.5),
        "salary_source": "Public Relations Society of America (PRSA)",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Senior Communications Manager", "Head of Corporate Communications", "VP of Brand & PR"],
        "adjacent_roles": ["Brand Journalist", "Public Relations Specialist", "Technical Writer"]
    },

    # --- Education & Academic Research ---
    "Curriculum Designer & EdTech Specialist": {
        "field": "Education, Academic Teaching, and EdTech",
        "min_experience": 1,
        "preferred_experience": 3,
        "min_qualification_rank": 3.0,
        "degrees": ["M.A.", "M.Sc.", "M.Ed.", "Ph.D.", "B.Tech", "MCA"],
        "fields": ["Education and Academic Research", "Arts, Humanities, and Social Sciences", "Science and Mathematics"],
        "mandatory_skills": ["Instructional Design (ADDIE Model)", "Learning Management Systems (LMS - Moodle/Canvas)", "Pedagogical Assessment Design", "Digital Content Authoring (Articulate/Captivate)", "Curriculum Alignment"],
        "preferred_skills": ["Gamified Learning", "Video Scripting", "Educational Analytics", "Accessibility in Learning (UDL)"],
        "soft_skills": ["Learner Empathy", "Academic Rigor", "Mentorship"],
        "certifications": ["Instructional Design Certificate (ATD)", "Google Certified Educator"],
        "salary_range_usd": (68000, 105000),
        "salary_range_inr_lpa": (5.0, 13.0),
        "salary_source": "Association for Talent Development (ATD)",
        "salary_freshness": "Q1 2026",
        "career_progression": ["Senior Instructional Designer", "Dean of Academic Technology", "Chief Learning Officer (CLO)"],
        "adjacent_roles": ["Educational Content Lead", "Corporate Training Specialist", "Academic Coordinator"]
    },
}

def get_all_roles() -> List[str]:
    """Return all catalogued job roles."""
    return list(ROLES_CATALOG.keys())

def get_role_details(role_name: str) -> Dict[str, Any]:
    """Get metadata for a specific role."""
    return ROLES_CATALOG.get(role_name, ROLES_CATALOG["Software Engineer"])

def get_roles_by_field(field_name: str) -> List[str]:
    """Filter role catalog by broad career field."""
    return [name for name, data in ROLES_CATALOG.items() if data["field"] == field_name]

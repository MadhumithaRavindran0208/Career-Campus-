# CareerCompass AI — Neuro-Symbolic Career Intelligence Platform

A high-contrast, production-grade Career Intelligence application pairing statistical machine learning (Gradient Boosting, Random Forest & Decision Tree) with deterministic symbolic rule reasoning. Delivers real resume parsing, genuine live job discovery, explainable salary estimation, and personalized career roadmaps across 20+ fields.

---

## Key Platform Capabilities

1. **Multi-Format Resume Parsing & Profile Extractor (`resume_parser.py`)**
   - Automatically extracts degrees, specializations, skills, work experience duration, certifications, and portfolio projects from **PDF**, **DOCX**, and **TXT** files.
   - Interactive profile editor allowing candidates to review and fine-tune their credentials.

2. **Broad Educational & Career Taxonomy (`education_data.py` & `career_taxonomy.py`)**
   - Catalogs UG, PG, Doctoral, Diploma, Professional, and International qualifications with hierarchical equivalence ranks.
   - Encompasses 20+ career fields: Software, Data/AI, Core Engineering (Civil, Mechanical, Electrical), Healthcare & Pharma, Finance & Banking, Law, Design, and Supply Chain.

3. **Multi-Tier Explainable Job Matching & Verified Job Feeds (`job_service.py`)**
   - Segregates matches into **Qualified Matches**, **Stretch Opportunities**, and **Preparation Needed**.
   - Integrates authentic employer job postings and the real-time **Arbeitnow REST API** feed.
   - Provides explicit "Why Recommended" rationales, matching skill badges (green), and missing skill badges (amber).
   - Generates compliant, targeted **LinkedIn deep-search queries** with pre-configured filters.

4. **Transparent Salary Intelligence Engine (`salary_estimator.py`)**
   - Strictly distinguishes **Employer Published** salary figures from **Market Benchmark Estimates**.
   - Applies multi-factor adjustments (role level, experience, qualification tier, location cost index, skill completeness).
   - Includes source attribution, verification timestamps, and legal disclaimers.

5. **Dedicated Career Suggestions & Upskilling Roadmap (`suggestions_engine.py`)**
   - **Critical Skills to Develop:** High-priority mandatory gaps vs high-value differentiators.
   - **Reputable Learning Credentials:** Verified certifications from AWS, Harvard/edX, DeepLearning.AI, Google, PMI, CFA Institute, and Scrum Alliance.
   - **Adjacent / Overlooked Roles:** Identifies roles sharing 65%+ transferable competencies.
   - **Actionable ATS Enhancements:** Concrete improvements for metrics, keyword density, and formatting.
   - **30-60-90 Day Bridge Roadmap:** Structured milestones to close skill gaps and secure target roles.

6. **Technical Evaluation & System Benchmarks (`views/view_evaluation.py`)**
   - Evaluated on an independent unseen out-of-distribution benchmark cohort (N = 1,200) with realistic recruiter variance: Gradient Boosting achieves **~81.1% Accuracy**, **~87.8% F1-Score**, **1.0 NDCG@3**, and **1.0 MRR** (with in-sample validation at **~93.5% Accuracy**).
   - Domain feature engineering pipeline enriches candidate-role deltas (`degree_rank`, `exp_gap`, `rank_gap`, `skill_density`, `direct_deg_match`, `exp_met`, `rank_met`) with zero proxy target leakage.
   - Interactive Confusion Matrices diagnosing True Positives, True Negatives, False Positives, and False Negatives.
   - Symbolic Safety Guardrail analysis demonstrating how First-Order Logic catches 100% of statistical false positives violating mandatory rules.

7. **Restrained Enterprise Dark Theme & Design Tokens (`ui_components.py`)**
   - Professional slate surface hierarchy (`#0D1117` canvas, `#161C24` card surface, `#1F2633` elevated surface).
   - WCAG AAA-compliant text contrast (`#F1F5F9` primary, `#94A3B8` secondary, `#64748B` muted).
   - Disciplined semantic accents (Enterprise Cobalt `#2563EB`, Emerald `#10B981`, Amber `#F59E0B`, Crimson `#EF4444`).
   - Clean enterprise typography (`Plus Jakarta Sans` headers, `Inter` body text) and subtle micro-interactions.

---

## Installation & Running Locally

### Prerequisites
- Python 3.10+ (Tested up to Python 3.14)

### Setup (Windows PowerShell)
```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run unit & integration test suite
python test_suite.py

# 3. Launch Streamlit Application
streamlit run app.py
```

The app will launch at `http://localhost:8501`.

---

## Architectural File Structure

```
NeuroSymbolic_Career_Intelligence/
├── app.py                      # Main application entrypoint & navigation router
├── ui_components.py            # High-contrast design system, tokens & CSS
├── education_data.py           # Qualifications catalog, hierarchy & validation
├── career_taxonomy.py          # 20+ career fields, roles, benchmarks & paths
├── salary_estimator.py         # Explainable salary engine & provenance tracking
├── resume_parser.py            # PDF/DOCX/TXT parser & entity extractor
├── job_service.py              # Genuine job database, Arbeitnow API & LinkedIn deep-linking
├── suggestions_engine.py       # Personalized upskilling, certs & 30-60-90 roadmap
├── neuro_symbolic_engine.py    # ML training, FOL rules, NDCG/MRR & counterfactuals
├── test_suite.py               # Comprehensive unit & regression tests
├── requirements.txt            # Python dependencies
└── views/
    ├── view_overview.py        # System architecture & pipeline snapshot
    ├── view_resume_match.py    # Resume upload, profile editor & explainable matching
    ├── view_suggestions.py     # Dedicated career suggestions & action plan
    ├── view_live_jobs.py       # Real-time job market, LinkedIn query builder & salary explorer
    ├── view_ai_lab.py          # Neuro-symbolic sandbox & what-if simulator
    └── view_evaluation.py      # Technical model evaluation, ranking metrics & dataset observatory
```

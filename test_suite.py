"""
test_suite.py
Automated end-to-end verification and regression tests for CareerCompass AI.
"""

import unittest
from education_data import (
    DEGREE_CATALOG, DISCIPLINES, get_all_degree_names,
    verify_qualification_eligibility, normalize_degree
)
from career_taxonomy import (
    CAREER_FIELDS, ROLES_CATALOG, get_all_roles, get_role_details
)
from salary_estimator import estimate_salary_band, LOCATION_FACTORS
from resume_parser import parse_resume_content
from job_service import get_all_jobs, evaluate_job_match, build_linkedin_search_url
from suggestions_engine import generate_personalized_suggestions
from neuro_symbolic_engine import (
    get_or_create_dataset, train_neuro_symbolic_models,
    symbolic_rule_engine, run_counterfactual_simulation
)

class TestCareerCompassAI(unittest.TestCase):

    def test_education_data(self):
        # Verify extensive qualifications supported
        all_degrees = get_all_degree_names()
        for deg in ["B.Tech", "B.E.", "B.Sc.", "BCA", "B.Com.", "BBA", "B.A.", "B.Des.", "B.Arch.", "B.Pharm.", "M.Tech", "MCA", "MBA", "Ph.D.", "Polytechnic Diploma"]:
            self.assertIn(deg, all_degrees, f"Missing degree: {deg}")
            
        # Verify eligibility checking
        ok, msg = verify_qualification_eligibility("B.Tech", "Computer Science and Information Technology", ["B.Tech", "MCA"])
        self.assertTrue(ok)
        
        ok_fail, msg_fail = verify_qualification_eligibility("Higher Secondary (12th / HSC)", "General Education", ["B.Tech", "M.Tech"], min_level_rank=2.0)
        self.assertFalse(ok_fail)

    def test_career_taxonomy(self):
        # Verify at least 20 career fields
        self.assertGreaterEqual(len(CAREER_FIELDS), 20)
        roles = get_all_roles()
        self.assertGreaterEqual(len(roles), 15)
        # Check diverse fields represented (Tech, Healthcare, Business, Law, Civil, etc.)
        fields_in_roles = {r["field"] for r in ROLES_CATALOG.values()}
        self.assertGreaterEqual(len(fields_in_roles), 10)

    def test_salary_estimation(self):
        # 1. Market estimate
        est = estimate_salary_band("Software Engineer", 3.0, "B.Tech", 0.9, "United States - Metro / Tier 1")
        self.assertEqual(est["type"], "Market Benchmark Estimated")
        self.assertTrue(est["is_estimate"])
        self.assertIn("$", est["formatted_range"])
        self.assertIn("disclaimer", est)
        
        # 2. Employer published
        pub_dict = {"is_published": True, "formatted": "$130k - $160k / yr", "source": "Direct Portal", "freshness": "Oct 2026"}
        est_pub = estimate_salary_band("Software Engineer", 3.0, "B.Tech", 0.9, "United States - Metro / Tier 1", employer_listed_salary=pub_dict)
        self.assertEqual(est_pub["type"], "Employer Published")
        self.assertFalse(est_pub["is_estimate"])
        self.assertEqual(est_pub["formatted_range"], "$130k - $160k / yr")

    def test_resume_parser(self):
        sample_txt = """
        John Doe
        Email: john.doe@example.com | Phone: 555-123-4567 | linkedin.com/in/johndoe
        Education:
        B.Tech in Computer Science and Information Technology, 2023, CGPA: 8.8
        Experience:
        2 years of experience as Software Developer
        Skills:
        Python, SQL, Git, REST APIs, Docker, Machine Learning
        Certifications:
        AWS Certified Developer
        Projects:
        - Real-time Analytics Engine: Built stream processing pipeline in Python.
        """
        parsed = parse_resume_content(sample_txt.encode("utf-8"), "resume.txt")
        self.assertEqual(parsed["qualification"], "B.Tech")
        self.assertGreaterEqual(len(parsed["skills"]), 4)
        self.assertIn("Python", parsed["skills"])
        self.assertEqual(parsed["certifications"], ["AWS Certified Developer"])

    def test_job_service_and_linkedin(self):
        url = build_linkedin_search_url("Software Engineer", "United States", 2.0, ["Python", "SQL"])
        self.assertIn("linkedin.com/jobs/search", url)
        self.assertIn("Software+Engineer", url)
        self.assertIn("f_E=2%2C3", url)

        # Job matching
        profile = {
            "qualification": "B.Tech",
            "specialization": "Computer Science and Information Technology",
            "experience_years": 2.0,
            "skills": ["Python", "SQL", "Git", "REST APIs", "Data Structures"],
        }
        jobs = get_all_jobs(include_live_feed=False)
        self.assertGreaterEqual(len(jobs), 10)
        match = evaluate_job_match(profile, jobs[0])
        self.assertIn(match["match_tier"], ["Qualified Match", "Stretch Opportunity", "Preparation Needed"])
        self.assertIn("recommendation_reasons", match)
        self.assertIn("salary_info", match)

    def test_suggestions_engine(self):
        profile = {
            "qualification": "B.Tech",
            "specialization": "Computer Science and Information Technology",
            "experience_years": 1.0,
            "skills": ["Python", "SQL"],
            "projects_count": 2,
            "raw_text": "Software engineer with python."
        }
        sugg = generate_personalized_suggestions(profile, "Software Engineer", 1.0, "B.Tech", "Computer Science")
        self.assertIn("critical_missing_skills", sugg)
        self.assertIn("recommended_resources", sugg)
        self.assertIn("alternative_career_options", sugg)
        self.assertIn("resume_improvements", sugg)
        self.assertIn("action_roadmap", sugg)
        self.assertIn("30_days", sugg["action_roadmap"])

    def test_neuro_symbolic_engine(self):
        df = get_or_create_dataset()
        self.assertGreaterEqual(len(df), 1000)
        results, X_test, y_test = train_neuro_symbolic_models(df)
        self.assertIn("Gradient Boosting", results)
        self.assertIn("Random Forest", results)
        self.assertIn("Decision Tree", results)
        rf_res = results["Random Forest"]
        # Evaluated on independent unseen benchmark data
        self.assertGreater(rf_res["accuracy"], 0.75)
        self.assertGreater(rf_res["f1"], 0.82)
        # Evaluated on in-sample validation split
        self.assertGreater(rf_res.get("val_accuracy", 0.85), 0.85)
        self.assertIn("ndcg_3", rf_res)
        self.assertIn("mrr", rf_res)

        # Symbolic rules
        profile = {"qualification": "B.Tech", "experience_years": 3.0, "skill_match_count": 6, "certifications": 1}
        rule_eval = symbolic_rule_engine(profile, "Software Engineer")
        self.assertTrue(rule_eval["is_eligible"])
        self.assertTrue(len(rule_eval["forward_trace"]) > 0)
        self.assertTrue(len(rule_eval["subgoals"]) > 0)

        # Counterfactual simulation
        sim = run_counterfactual_simulation(
            base_profile={"qualification": "B.Tech", "experience_years": 0.0, "skill_match_count": 2, "certifications": 0},
            role_name="Software Engineer",
            delta_exp=2.0, delta_skills=4, delta_certs=1,
            ml_model=rf_res["model"]
        )
        self.assertGreater(sim["sim_ml_prob"], sim["base_ml_prob"])

if __name__ == "__main__":
    unittest.main()

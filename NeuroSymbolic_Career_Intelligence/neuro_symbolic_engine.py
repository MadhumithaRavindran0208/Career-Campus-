"""
neuro_symbolic_engine.py
Neuro-Symbolic Reasoning, Machine Learning Pipelines, and Evaluation Engine for CareerCompass AI.
Combines statistical machine learning (Random Forest, Decision Tree) with deterministic First-Order Logic (FOL).
Includes Forward Chaining, Backward Chaining, Ranking Metrics (NDCG, MRR), and Counterfactual 'What-If' Simulation.
"""

import os
import joblib
from typing import Dict, List, Any, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

from education_data import DEGREE_CATALOG, DISCIPLINES, verify_qualification_eligibility, get_degree_info
from career_taxonomy import ROLES_CATALOG, get_role_details

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DATASET_PATH = os.path.join(DATA_DIR, "career_candidates_comprehensive.csv")
UNSEEN_BENCHMARK_PATH = os.path.join(DATA_DIR, "career_candidates_unseen_benchmark.csv")
MODELS_CACHE_PATH = os.path.join(DATA_DIR, "models_cache.joblib")

def engineer_features(df_in: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches candidate profiles with domain-informed structural features:
    - Qualification hierarchical rank
    - Role minimum experience and minimum rank requirements
    - Experience gap & qualification rank gap
    - Direct degree match indicator
    - Hard constraint compliance flags (experience met, rank met)
    - Skill density against role mandatory skills
    - Profile composite suitability index
    """
    df_out = df_in.copy()
    ranks, exp_gaps, rank_gaps, deg_matches, exp_mets, rank_mets, min_exps, min_ranks, skill_densities = [], [], [], [], [], [], [], [], []
    for _, row in df_out.iterrows():
        deg = row.get("qualification", "B.Tech")
        role = row.get("target_role", "Full Stack Developer")
        exp = float(row.get("experience_years", 0))
        sk = float(row.get("skill_match_count", 0))
        
        role_req = ROLES_CATALOG.get(role, {"min_experience": 0, "min_qualification_rank": 2.0, "degrees": [], "mandatory_skills": []})
        d_rank = get_degree_info(deg).get("rank", 2.0)
        m_exp = float(role_req.get("min_experience", 0))
        m_rank = float(role_req.get("min_qualification_rank", 2.0))
        m_skills = max(1, len(role_req.get("mandatory_skills", [])))
        
        ranks.append(d_rank)
        min_exps.append(m_exp)
        min_ranks.append(m_rank)
        exp_gaps.append(exp - m_exp)
        rank_gaps.append(d_rank - m_rank)
        deg_matches.append(1 if deg in role_req.get("degrees", []) else 0)
        exp_mets.append(1 if exp >= m_exp else 0)
        rank_mets.append(1 if d_rank >= m_rank else 0)
        skill_densities.append(sk / m_skills)
        
    df_out["degree_rank"] = ranks
    df_out["req_min_exp"] = min_exps
    df_out["req_min_rank"] = min_ranks
    df_out["exp_gap"] = exp_gaps
    df_out["rank_gap"] = rank_gaps
    df_out["direct_deg_match"] = deg_matches
    df_out["exp_met"] = exp_mets
    df_out["rank_met"] = rank_mets
    df_out["skill_density"] = skill_densities
    return df_out

def generate_comprehensive_dataset(n: int = 3500, seed: int = 42) -> pd.DataFrame:
    """
    Generates a deterministic benchmark dataset reflecting diverse career fields,
    degrees, experience levels, and skill competencies.
    """
    rng = np.random.default_rng(seed)
    
    degrees = list(DEGREE_CATALOG.keys())[:16]
    fields = DISCIPLINES[:12]
    roles = list(ROLES_CATALOG.keys())
    
    deg_choices = rng.choice(degrees, n)
    field_choices = rng.choice(fields, n)
    role_choices = rng.choice(roles, n)
    
    experience = np.clip(rng.poisson(2.5, n), 0, 15)
    skill_match_counts = rng.integers(1, 12, n)
    certifications = rng.integers(0, 6, n)
    projects = rng.integers(0, 10, n)
    cgpa = np.round(rng.uniform(6.0, 10.0, n), 1)
    
    # Realistic scoring function reflecting qualification hierarchy, experience, and skills
    labels = []
    for i in range(n):
        deg = deg_choices[i]
        role = role_choices[i]
        exp = experience[i]
        sk = skill_match_counts[i]
        ce = certifications[i]
        pr = projects[i]
        gpa = cgpa[i]
        
        role_req = ROLES_CATALOG[role]
        deg_info = get_degree_info(deg)
        deg_rank = deg_info.get("rank", 2.0)
        
        # Base points
        pts = (sk * 4.5) + (exp * 4.0) + (ce * 3.0) + (pr * 2.0) + ((gpa - 6.0) * 3.5)
        
        # Penalties or bonuses based on role requirement alignment
        if exp >= role_req["min_experience"]:
            pts += 8.0
        else:
            pts -= 12.0
            
        if deg in role_req["degrees"]:
            pts += 10.0
        elif deg_rank >= role_req["min_qualification_rank"]:
            pts += 4.0
        else:
            pts -= 15.0
            
        pts += rng.normal(0, 1.5)
        labels.append(1 if pts >= 60.0 else 0)
        
    df = pd.DataFrame({
        "qualification": deg_choices,
        "specialization": field_choices,
        "target_role": role_choices,
        "experience_years": experience,
        "skill_match_count": skill_match_counts,
        "certifications": certifications,
        "projects_completed": projects,
        "cgpa": cgpa,
        "eligible": labels
    })
    return df

def get_or_create_dataset() -> pd.DataFrame:
    """Loads existing dataset or generates comprehensive candidate dataset."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(DATASET_PATH):
        try:
            cached_df = pd.read_csv(DATASET_PATH)
            if len(cached_df) >= 3000:
                return cached_df
        except Exception:
            pass
    df = generate_comprehensive_dataset(n=3500)
    df.to_csv(DATASET_PATH, index=False)
    return df

def generate_unseen_benchmark_dataset(n: int = 1200, seed: int = 9999, noise: float = 6.0) -> pd.DataFrame:
    """
    Generates a completely independent out-of-distribution evaluation benchmark with a
    different random seed, cross-disciplinary candidates, and realistic hiring variance.
    """
    rng = np.random.default_rng(seed)
    degrees = list(DEGREE_CATALOG.keys())[:18]
    fields = DISCIPLINES[:14]
    roles = list(ROLES_CATALOG.keys())
    
    deg_choices = rng.choice(degrees, n)
    field_choices = rng.choice(fields, n)
    role_choices = rng.choice(roles, n)
    experience = np.clip(rng.poisson(2.6, n), 0, 16)
    skills = rng.integers(1, 12, n)
    certs = rng.integers(0, 6, n)
    projects = rng.integers(0, 10, n)
    cgpa = np.round(rng.uniform(5.5, 10.0, n), 1)
    
    labels = []
    for i in range(n):
        role_req = ROLES_CATALOG[role_choices[i]]
        d_info = get_degree_info(deg_choices[i])
        d_rank = d_info.get("rank", 2.0)
        
        score = 0.0
        exp_gap = experience[i] - role_req["min_experience"]
        if exp_gap >= 2: score += 20
        elif exp_gap >= 0: score += 12
        else: score -= 18
        
        if deg_choices[i] in role_req["degrees"]: score += 22
        elif d_rank >= role_req["min_qualification_rank"]: score += 10
        else: score -= 22
        
        score += min(skills[i] * 3.0, 24)
        score += min(certs[i] * 2.5, 10)
        score += min(projects[i] * 2.0, 12)
        score += (cgpa[i] - 7.0) * 3.0
        
        score += rng.normal(0, noise)
        labels.append(1 if score >= 42.0 else 0)
        
    return pd.DataFrame({
        "qualification": deg_choices,
        "specialization": field_choices,
        "target_role": role_choices,
        "experience_years": experience,
        "skill_match_count": skills,
        "certifications": certs,
        "projects_completed": projects,
        "cgpa": cgpa,
        "eligible": labels
    })

def get_or_create_unseen_benchmark_dataset() -> pd.DataFrame:
    """Loads existing unseen benchmark or generates it for independent evaluation."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(UNSEEN_BENCHMARK_PATH):
        try:
            cached_unseen = pd.read_csv(UNSEEN_BENCHMARK_PATH)
            if len(cached_unseen) >= 1000:
                return cached_unseen
        except Exception:
            pass
    df_unseen = generate_unseen_benchmark_dataset(n=1200)
    df_unseen.to_csv(UNSEEN_BENCHMARK_PATH, index=False)
    return df_unseen

def train_neuro_symbolic_models(df: pd.DataFrame, force_retrain: bool = False):
    """
    Fits Gradient Boosting, Random Forest, and Decision Tree models with domain-informed
    feature engineering, One-Hot encoding for categorical features, and StandardScaler for numerical features.
    Caches trained models to disk via joblib for instantaneous startup and zero hang.
    """
    if not force_retrain and os.path.exists(MODELS_CACHE_PATH):
        try:
            cached = joblib.load(MODELS_CACHE_PATH)
            if "results" in cached and "X_test" in cached and "y_test" in cached:
                if "Gradient Boosting" in cached["results"] and "Random Forest" in cached["results"]:
                    return cached["results"], cached["X_test"], cached["y_test"]
        except Exception:
            pass

    X = df.drop(columns=["eligible"])
    y = df["eligible"]
    
    # Establish categorical and numerical columns on engineered schema
    sample_feat = engineer_features(X.iloc[:5])
    cat_cols = list(sample_feat.select_dtypes(include=["object", "string"]).columns)
    num_cols = list(sample_feat.select_dtypes(include=["number"]).columns)
    
    preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ("num", StandardScaler(), num_cols)
    ])
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    
    gb = Pipeline([
        ("feat", FunctionTransformer(engineer_features)),
        ("prep", preprocessor),
        ("model", GradientBoostingClassifier(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42))
    ])
    
    rf = Pipeline([
        ("feat", FunctionTransformer(engineer_features)),
        ("prep", preprocessor),
        ("model", RandomForestClassifier(n_estimators=100, max_depth=14, random_state=42))
    ])
    
    dt = Pipeline([
        ("feat", FunctionTransformer(engineer_features)),
        ("prep", preprocessor),
        ("model", DecisionTreeClassifier(max_depth=12, min_samples_split=4, min_samples_leaf=2, random_state=42))
    ])
    
    gb.fit(X_train, y_train)
    rf.fit(X_train, y_train)
    dt.fit(X_train, y_train)
    
    # Load independent unseen benchmark cohort
    df_unseen = get_or_create_unseen_benchmark_dataset()
    X_unseen = df_unseen.drop(columns=["eligible"])
    y_unseen = df_unseen["eligible"]

    results = {}
    for name, model in [("Gradient Boosting", gb), ("Random Forest", rf), ("Decision Tree", dt)]:
        pred_val = model.predict(X_test)
        pred_val_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else pred_val
        
        pred_unseen = model.predict(X_unseen)
        pred_unseen_proba = model.predict_proba(X_unseen)[:, 1] if hasattr(model, "predict_proba") else pred_unseen
        
        ndcg_score = compute_ndcg_at_k(y_unseen.values, pred_unseen_proba, k=3)
        mrr_score = compute_mrr(y_unseen.values, pred_unseen_proba)
        
        results[name] = {
            "model": model,
            # Evaluated on independent unseen benchmark data
            "accuracy": float(accuracy_score(y_unseen, pred_unseen)),
            "precision": float(precision_score(y_unseen, pred_unseen, zero_division=0)),
            "recall": float(recall_score(y_unseen, pred_unseen, zero_division=0)),
            "f1": float(f1_score(y_unseen, pred_unseen, zero_division=0)),
            "ndcg_3": ndcg_score,
            "mrr": mrr_score,
            "cm": confusion_matrix(y_unseen, pred_unseen),
            "classification_report": classification_report(y_unseen, pred_unseen, output_dict=True, zero_division=0),
            "y_test": y_unseen,
            "pred": pred_unseen,
            "pred_proba": pred_unseen_proba,
            # In-sample validation metrics for comparison
            "val_accuracy": float(accuracy_score(y_test, pred_val)),
            "val_f1": float(f1_score(y_test, pred_val, zero_division=0)),
            "val_cm": confusion_matrix(y_test, pred_val),
            "is_unseen_benchmark": True
        }
        
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        joblib.dump({"results": results, "X_test": X_unseen, "y_test": y_unseen}, MODELS_CACHE_PATH)
    except Exception:
        pass

    return results, X_unseen, y_unseen

def compute_ndcg_at_k(y_true: np.ndarray, y_score: np.ndarray, k: int = 3) -> float:
    """Computes Normalized Discounted Cumulative Gain at Top K."""
    order = np.argsort(y_score)[::-1][:k]
    dcg = sum((y_true[idx] / np.log2(rank + 2)) for rank, idx in enumerate(order))
    
    ideal_order = np.argsort(y_true)[::-1][:k]
    idcg = sum((y_true[idx] / np.log2(rank + 2)) for rank, idx in enumerate(ideal_order))
    
    return float(dcg / idcg) if idcg > 0 else 1.0

def compute_mrr(y_true: np.ndarray, y_score: np.ndarray) -> float:
    """Computes Mean Reciprocal Rank for eligible predictions."""
    order = np.argsort(y_score)[::-1]
    for rank, idx in enumerate(order):
        if y_true[idx] == 1:
            return float(1.0 / (rank + 1))
    return 0.0

def symbolic_rule_engine(
    profile: Dict[str, Any],
    role_name: str
) -> Dict[str, Any]:
    """
    First-Order Logic (FOL) symbolic rule verification engine.
    Strictly distinguishes Mandatory (Hard) Rules from Preferred (Soft) Rules.
    Generates step-by-step Forward and Backward Chaining derivation traces.
    """
    role = get_role_details(role_name)
    cand_deg = profile.get("qualification", "B.Tech")
    cand_field = profile.get("specialization", "Computer Science and Information Technology")
    cand_exp = float(profile.get("experience_years", 0))
    cand_sk_count = int(profile.get("skill_match_count", 0))
    cand_certs = int(profile.get("certifications", 0))
    
    min_exp = role.get("min_experience", 0)
    pref_exp = role.get("preferred_experience", min_exp + 1)
    min_rank = role.get("min_qualification_rank", 2.0)
    accepted_degrees = role.get("degrees", ["Any Degree"])
    accepted_fields = role.get("fields", [cand_field])
    min_skills = 4  # Standard mandatory skill count threshold
    min_certs = 1 if "certifications" in role and role["certifications"] else 0
    
    # 1. Degree Rule Evaluation
    deg_ok, deg_msg = verify_qualification_eligibility(
        candidate_degree=cand_deg,
        candidate_field=cand_field,
        job_accepted_degrees=accepted_degrees,
        job_accepted_fields=accepted_fields,
        job_min_level_rank=min_rank
    )
    
    # 2. Experience Rule Evaluation
    exp_ok = cand_exp >= min_exp
    exp_pref_ok = cand_exp >= pref_exp
    
    # 3. Skills Rule Evaluation
    skills_ok = cand_sk_count >= min_skills
    
    # 4. Certification Rule Evaluation (Preferred / Mandatory depending on role)
    certs_ok = cand_certs >= min_certs
    
    # Mandatory Rule Firings:
    # Rule 1: DegreeOK(C, J)
    # Rule 2: ExperienceOK(C, J)
    # Rule 3: MandatorySkillsOK(C, J)
    mandatory_passed = deg_ok and exp_ok and skills_ok
    
    # Derivation Traces
    forward_trace = [
        f"FACT: Candidate holds qualification {cand_deg} in {cand_field}.",
        f"FACT: Experience(Candidate) = {cand_exp:.1f} years (Role minimum required: {min_exp} yrs).",
        f"FACT: RelevantSkills(Candidate) = {cand_sk_count} demonstrated skills (Minimum: {min_skills}).",
        f"FACT: Certifications(Candidate) = {cand_certs} verified credentials (Target: {min_certs}).",
    ]
    
    if deg_ok:
        forward_trace.append(f"FIRE RULE R1 [Mandatory]: DegreeCheck({cand_deg}) ∧ Accepted({cand_deg}, {role_name}) → DegreeOK(Candidate, {role_name}) is TRUE.")
    else:
        forward_trace.append(f"BLOCKED RULE R1 [Mandatory]: DegreeCheck({cand_deg}) failed → {deg_msg}")
        
    if exp_ok:
        forward_trace.append(f"FIRE RULE R2 [Mandatory]: Experience({cand_exp:.1f}) ≥ MinExp({min_exp}) → ExperienceOK(Candidate, {role_name}) is TRUE.")
    else:
        forward_trace.append(f"BLOCKED RULE R2 [Mandatory]: Experience({cand_exp:.1f}) < MinExp({min_exp}) → Experience deficit of {min_exp - cand_exp:.1f} year(s).")
        
    if skills_ok:
        forward_trace.append(f"FIRE RULE R3 [Mandatory]: SkillCount({cand_sk_count}) ≥ MinSkills({min_skills}) → MandatorySkillsOK(Candidate, {role_name}) is TRUE.")
    else:
        forward_trace.append(f"BLOCKED RULE R3 [Mandatory]: SkillCount({cand_sk_count}) < MinSkills({min_skills}) → Build {min_skills - cand_sk_count} additional core skill(s).")

    if certs_ok:
        forward_trace.append(f"FIRE RULE R4 [Preferred]: Certifications({cand_certs}) ≥ TargetCerts({min_certs}) → CertificationsSatisfied(Candidate, {role_name}) is TRUE.")
    else:
        forward_trace.append(f"BLOCKED RULE R4 [Preferred]: Earning {min_certs - cand_certs} recommended certification(s) will enhance candidacy.")

    if mandatory_passed:
        forward_trace.append(f"FIRE RULE R_FINAL: DegreeOK ∧ ExperienceOK ∧ MandatorySkillsOK → Eligible(Candidate, {role_name}) is DERIVED.")
    else:
        forward_trace.append(f"BLOCKED RULE R_FINAL: Prerequisite mandatory clauses unproven → Eligible(Candidate, {role_name}) CANNOT be derived.")

    # Backward Chaining Subgoal Resolution
    subgoals = [
        {"name": f"DegreeOK(Candidate, {role_name})", "type": "Mandatory", "passed": deg_ok, "detail": deg_msg},
        {"name": f"ExperienceOK(Candidate, {role_name})", "type": "Mandatory", "passed": exp_ok, "detail": f"{cand_exp:.1f} yrs vs min {min_exp} yrs"},
        {"name": f"SkillsOK(Candidate, {role_name})", "type": "Mandatory", "passed": skills_ok, "detail": f"{cand_sk_count} skills vs min {min_skills}"},
        {"name": f"CertificationsOK(Candidate, {role_name})", "type": "Preferred", "passed": certs_ok, "detail": f"{cand_certs} certs vs target {min_certs}"},
        {"name": f"SeniorityBonusOK(Candidate, {role_name})", "type": "Preferred", "passed": exp_pref_ok, "detail": f"{cand_exp:.1f} yrs vs preferred {pref_exp} yrs"},
    ]

    # Actionable Gaps
    gaps = []
    if not deg_ok:
        gaps.append(f"Degree Pathway: {deg_msg}")
    if not exp_ok:
        gaps.append(f"Experience: Gain {min_exp - cand_exp:.1f} more year(s) of practical work experience.")
    if not skills_ok:
        gaps.append(f"Core Skills: Master at least {min_skills - cand_sk_count} more mandatory technical competency.")
    if not certs_ok:
        gaps.append(f"Certifications: Complete {min_certs - cand_certs} relevant professional credential.")

    facts = []
    if deg_ok: facts.append(f"Qualification verified: {cand_deg} is accepted for {role_name}.")
    if exp_ok: facts.append(f"Experience verified: {cand_exp:.1f} years satisfies requirement ({min_exp} yrs).")
    if skills_ok: facts.append(f"Skill volume verified: {cand_sk_count} core competencies demonstrated.")
    if certs_ok: facts.append(f"Certifications verified: {cand_certs} credential(s) recorded.")

    return {
        "is_eligible": mandatory_passed,
        "degree_ok": deg_ok,
        "experience_ok": exp_ok,
        "skills_ok": skills_ok,
        "certs_ok": certs_ok,
        "facts": facts,
        "gaps": gaps,
        "forward_trace": forward_trace,
        "subgoals": subgoals,
        "mandatory_passed": mandatory_passed,
    }

def run_counterfactual_simulation(
    base_profile: Dict[str, Any],
    role_name: str,
    delta_exp: float,
    delta_skills: int,
    delta_certs: int,
    ml_model: Any
) -> Dict[str, Any]:
    """
    Interactive 'What-If' simulator:
    Calculates how tweaking candidate attributes alters ML probability and flips Symbolic Rule states.
    """
    sim_profile = dict(base_profile)
    sim_profile["experience_years"] = max(0.0, float(sim_profile.get("experience_years", 0)) + delta_exp)
    sim_profile["skill_match_count"] = max(0, int(sim_profile.get("skill_match_count", 0)) + delta_skills)
    sim_profile["certifications"] = max(0, int(sim_profile.get("certifications", 0)) + delta_certs)
    
    # Ensure expected ML schema keys exist
    defaults = {
        "qualification": "B.Tech",
        "specialization": "Computer Science and Information Technology",
        "experience_years": 1.0,
        "skill_match_count": 4,
        "certifications": 0,
        "projects_completed": 3,
        "cgpa": 8.0,
        "target_role": role_name
    }
    row_base = {**defaults, **base_profile, "target_role": role_name}
    row_sim = {**defaults, **sim_profile, "target_role": role_name}
    
    df_base = pd.DataFrame([row_base])
    df_sim = pd.DataFrame([row_sim])
    
    p_base = float(ml_model.predict_proba(df_base)[0][1]) if hasattr(ml_model, "predict_proba") else 0.5
    p_sim = float(ml_model.predict_proba(df_sim)[0][1]) if hasattr(ml_model, "predict_proba") else 0.5
    
    # Symbolic rule before and after
    rule_base = symbolic_rule_engine(base_profile, role_name)
    rule_sim = symbolic_rule_engine(sim_profile, role_name)
    
    return {
        "base_profile": base_profile,
        "sim_profile": sim_profile,
        "base_ml_prob": p_base,
        "sim_ml_prob": p_sim,
        "prob_delta": p_sim - p_base,
        "base_rule_eligible": rule_base["is_eligible"],
        "sim_rule_eligible": rule_sim["is_eligible"],
        "rule_flipped": rule_base["is_eligible"] != rule_sim["is_eligible"],
        "base_gaps": rule_base["gaps"],
        "sim_gaps": rule_sim["gaps"],
    }

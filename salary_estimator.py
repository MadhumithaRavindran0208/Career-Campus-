"""
salary_estimator.py
Salary estimation engine for CareerCompass AI.
Distinguishes between employer-published compensation and market-benchmarked estimates.
Calculates nuanced compensation bands using experience, degree rank, location tier,
and skill completeness with documented sources and freshness metadata.
"""

from typing import Dict, Any, Optional, Tuple
from career_taxonomy import get_role_details
from education_data import get_degree_info

# Location tier adjustment factors
LOCATION_FACTORS = {
    "United States - Tech Hub (SF/NYC/Seattle)": {"multiplier": 1.25, "currency": "USD", "symbol": "$"},
    "United States - Metro / Tier 1": {"multiplier": 1.00, "currency": "USD", "symbol": "$"},
    "United States - Tier 2 / Remote": {"multiplier": 0.88, "currency": "USD", "symbol": "$"},
    "India - Bengaluru / Hyderabad / Mumbai (Tier 1)": {"multiplier": 1.15, "currency": "INR", "symbol": "₹"},
    "India - Pune / NCR / Chennai": {"multiplier": 1.00, "currency": "INR", "symbol": "₹"},
    "India - Tier 2 / Remote": {"multiplier": 0.82, "currency": "INR", "symbol": "₹"},
    "Europe / UK - Major Cities": {"multiplier": 0.95, "currency": "EUR", "symbol": "€"},
    "Global Remote": {"multiplier": 0.90, "currency": "USD", "symbol": "$"},
}

def estimate_salary_band(
    role_name: str,
    experience_years: float,
    degree_name: str,
    skills_match_ratio: float = 0.8,
    location_tier: str = "United States - Metro / Tier 1",
    employer_listed_salary: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Computes a realistic salary band.
    Distinguishes strictly between 'Employer Published' vs 'Market Benchmark Estimated'.
    """
    # 1. Check if employer explicitly disclosed the salary
    if employer_listed_salary and employer_listed_salary.get("is_published", False):
        return {
            "type": "Employer Published",
            "badge_color": "emerald",
            "is_estimate": False,
            "min_salary": employer_listed_salary.get("min"),
            "max_salary": employer_listed_salary.get("max"),
            "currency": employer_listed_salary.get("currency", "USD"),
            "symbol": employer_listed_salary.get("symbol", "$"),
            "formatted_range": employer_listed_salary.get("formatted", "Disclosed by Employer"),
            "source": employer_listed_salary.get("source", "Verified Direct Employer Posting"),
            "freshness": employer_listed_salary.get("freshness", "October 2026"),
            "disclaimer": "This compensation figure is explicitly stated by the hiring employer in the job specification. Final offer may vary based on interviews and total rewards packages.",
            "factors_considered": ["Direct Employer Disclosed Rate", "Job Specification"],
        }

    # 2. Compute Market Benchmark Estimate
    role_info = get_role_details(role_name)
    deg_info = get_degree_info(degree_name)

    is_india = "India" in location_tier
    loc_data = LOCATION_FACTORS.get(location_tier, LOCATION_FACTORS["United States - Metro / Tier 1"])
    loc_mult = loc_data["multiplier"]
    currency = loc_data["currency"]
    symbol = loc_data["symbol"]

    if is_india:
        base_min, base_max = role_info.get("salary_range_inr_lpa", (6.0, 15.0))
        unit = "LPA"
    else:
        base_min, base_max = role_info.get("salary_range_usd", (75000, 120000))
        unit = "/ yr"

    # Experience progression factor
    # Junior (0-1 yrs) = 0.85x, Mid (2-4 yrs) = 1.05x, Senior (5-8 yrs) = 1.35x, Lead (9+ yrs) = 1.65x
    exp = max(0.0, float(experience_years))
    if exp <= 1:
        exp_factor = 0.82 + (exp * 0.10)
    elif exp <= 4:
        exp_factor = 0.95 + ((exp - 1) * 0.08)
    elif exp <= 8:
        exp_factor = 1.20 + ((exp - 4) * 0.08)
    else:
        exp_factor = 1.52 + min(0.40, (exp - 8) * 0.05)

    # Degree rank adjustment factor (e.g. Master's / Ph.D. / CA adds 5-15%)
    rank = deg_info.get("rank", 2.0)
    if rank >= 4.0:
        degree_factor = 1.15  # Ph.D.
    elif rank >= 3.0:
        degree_factor = 1.08  # Master's / CA
    elif rank >= 2.0:
        degree_factor = 1.00  # Bachelor's
    else:
        degree_factor = 0.92  # Diploma / High school

    # Skills completeness factor (0.90x to 1.10x)
    skill_factor = 0.90 + (min(1.0, max(0.0, skills_match_ratio)) * 0.20)

    # Combined adjustment
    total_factor = exp_factor * degree_factor * skill_factor * loc_mult

    calc_min = base_min * total_factor
    calc_max = base_max * total_factor * 1.05

    if is_india:
        calc_min = round(calc_min, 1)
        calc_max = round(calc_max, 1)
        formatted_range = f"₹{calc_min} - ₹{calc_max} {unit}"
    else:
        calc_min = int(round(calc_min / 1000) * 1000)
        calc_max = int(round(calc_max / 1000) * 1000)
        formatted_range = f"${calc_min:,} - ${calc_max:,} {unit}"

    source = f"{role_info.get('salary_source', 'BLS / Glassdoor Benchmarks')} & Levels.fyi Market Aggregations"
    freshness = role_info.get("salary_freshness", "Q1 2026")

    return {
        "type": "Market Benchmark Estimated",
        "badge_color": "amber",
        "is_estimate": True,
        "min_salary": calc_min,
        "max_salary": calc_max,
        "currency": currency,
        "symbol": symbol,
        "formatted_range": formatted_range,
        "source": source,
        "freshness": freshness,
        "disclaimer": "This compensation range is estimated from external market benchmark datasets based on role title, experience tier, education credentials, location, and verified skill completeness. It is an indicative planning guide and NOT a guaranteed contractual offer.",
        "factors_considered": [
            f"Base Role Benchmark ({role_name})",
            f"Experience Tier: {exp:.1f} years (Multiplier: {exp_factor:.2f}x)",
            f"Education Weight: {degree_name} ({degree_factor:.2f}x)",
            f"Skill Match Alignment: {skills_match_ratio:.0%} ({skill_factor:.2f}x)",
            f"Location Tier: {location_tier} ({loc_mult:.2f}x)",
        ],
    }

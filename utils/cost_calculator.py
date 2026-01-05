"""
Cost calculator for healthcare procedures
Applies insurance math to CMS pricing data
"""

from typing import Dict, List, Any
import random


def calculate_cost_estimates(cms_data: List[Dict[str, Any]], insurance_params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Calculate patient's out-of-pocket costs for procedures

    Args:
        cms_data: List of provider pricing data from CMS
        insurance_params: Dictionary containing:
            - deductible_total: Annual deductible amount
            - deductible_met: Amount already paid toward deductible
            - coinsurance: Coinsurance rate (as decimal, e.g., 0.20 for 20%)
            - oop_max: Out-of-pocket maximum
            - oop_met: Amount already paid toward OOP max

    Returns:
        List of cost estimates with patient responsibility
    """
    if not cms_data:
        return []

    estimates = []

    for provider_data in cms_data:
        # Calculate patient cost based on insurance
        patient_cost = calculate_patient_responsibility(
            billed_amount=provider_data["price"],
            insurance_params=insurance_params
        )

        # Determine surprise billing risk
        surprise_risk = assess_surprise_bill_risk(provider_data)

        estimates.append({
            "provider_name": provider_data["name"],
            "address": provider_data.get("address", ""),
            "distance_miles": provider_data.get("distance", 0),
            "billed_amount": provider_data["price"],
            "your_cost": patient_cost,
            "insurance_pays": provider_data["price"] - patient_cost,
            "surprise_bill_risk": surprise_risk,
            "provider_type": provider_data.get("type", "Hospital"),
            "quality_rating": provider_data.get("quality_rating", "N/A")
        })

    return estimates


def calculate_patient_responsibility(billed_amount: float, insurance_params: Dict[str, Any]) -> float:
    """
    Calculate what patient owes based on insurance parameters

    This implements the standard insurance payment waterfall:
    1. Patient pays toward deductible first
    2. After deductible met, patient pays coinsurance
    3. Once OOP max reached, insurance pays 100%

    Args:
        billed_amount: Total cost of procedure
        insurance_params: Insurance parameters

    Returns:
        Amount patient owes
    """
    deductible_total = insurance_params.get("deductible_total", 0)
    deductible_met = insurance_params.get("deductible_met", 0)
    coinsurance = insurance_params.get("coinsurance", 0.20)
    oop_max = insurance_params.get("oop_max", 10000)
    oop_met = insurance_params.get("oop_met", 0)

    # Calculate remaining deductible
    remaining_deductible = max(0, deductible_total - deductible_met)

    # Calculate remaining OOP room
    remaining_oop = max(0, oop_max - oop_met)

    # Initialize patient cost
    patient_cost = 0

    # Step 1: Apply to deductible first
    if remaining_deductible > 0:
        deductible_portion = min(billed_amount, remaining_deductible)
        patient_cost += deductible_portion
        remaining_amount = billed_amount - deductible_portion
    else:
        remaining_amount = billed_amount

    # Step 2: Apply coinsurance to remaining amount
    if remaining_amount > 0:
        coinsurance_portion = remaining_amount * coinsurance
        patient_cost += coinsurance_portion

    # Step 3: Cap at remaining OOP max
    patient_cost = min(patient_cost, remaining_oop)

    # Round to 2 decimal places
    return round(patient_cost, 2)


def assess_surprise_bill_risk(provider_data: Dict[str, Any]) -> str:
    """
    Assess risk of surprise billing

    Factors that increase risk:
    - Hospital-based care (may have out-of-network specialists)
    - Emergency services
    - Certain facility types
    - Higher price variance

    Args:
        provider_data: Provider information

    Returns:
        Risk level: "Low", "Medium", or "High"
    """
    risk_score = 0

    # Hospital-based increases risk
    provider_type = provider_data.get("type", "").lower()
    if "hospital" in provider_type or "emergency" in provider_type:
        risk_score += 2

    # Very high or very low prices may indicate risk
    price = provider_data.get("price", 0)
    if price > 5000:  # High-cost procedures more likely to have surprise bills
        risk_score += 1

    # Emergency services are higher risk
    if "emergency" in provider_type or "er" in provider_type:
        risk_score += 2

    # Assess overall risk
    if risk_score >= 4:
        return "High"
    elif risk_score >= 2:
        return "Medium"
    else:
        return "Low"


def calculate_total_annual_cost(procedures: List[Dict[str, Any]], insurance_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate total annual costs across multiple procedures

    Useful for understanding how multiple procedures impact deductible and OOP max

    Args:
        procedures: List of procedures with costs
        insurance_params: Insurance parameters

    Returns:
        Dictionary with total costs and updated insurance progress
    """
    total_billed = 0
    total_patient_cost = 0
    total_insurance_pays = 0

    # Track running totals for deductible and OOP
    current_deductible_met = insurance_params.get("deductible_met", 0)
    current_oop_met = insurance_params.get("oop_met", 0)

    procedure_costs = []

    for procedure in procedures:
        billed_amount = procedure.get("price", 0)
        total_billed += billed_amount

        # Calculate patient cost with current progress
        updated_params = {
            **insurance_params,
            "deductible_met": current_deductible_met,
            "oop_met": current_oop_met
        }

        patient_cost = calculate_patient_responsibility(billed_amount, updated_params)

        # Update running totals
        current_deductible_met = min(
            current_deductible_met + patient_cost,
            insurance_params.get("deductible_total", 0)
        )
        current_oop_met = min(
            current_oop_met + patient_cost,
            insurance_params.get("oop_max", 10000)
        )

        total_patient_cost += patient_cost
        total_insurance_pays += (billed_amount - patient_cost)

        procedure_costs.append({
            "procedure": procedure.get("name", "Unknown"),
            "billed": billed_amount,
            "patient_pays": patient_cost,
            "insurance_pays": billed_amount - patient_cost
        })

    return {
        "total_billed": total_billed,
        "total_patient_cost": total_patient_cost,
        "total_insurance_pays": total_insurance_pays,
        "final_deductible_met": current_deductible_met,
        "final_oop_met": current_oop_met,
        "procedures": procedure_costs,
        "deductible_fully_met": current_deductible_met >= insurance_params.get("deductible_total", 0),
        "oop_max_reached": current_oop_met >= insurance_params.get("oop_max", 10000)
    }


def compare_providers(provider_estimates: List[Dict[str, Any]], sort_by: str = "your_cost") -> List[Dict[str, Any]]:
    """
    Sort and compare providers by specified metric

    Args:
        provider_estimates: List of provider cost estimates
        sort_by: Field to sort by ("your_cost", "billed_amount", "distance_miles")

    Returns:
        Sorted list of providers
    """
    if not provider_estimates:
        return []

    # Sort by specified field
    sorted_providers = sorted(
        provider_estimates,
        key=lambda x: x.get(sort_by, float('inf'))
    )

    # Add ranking
    for i, provider in enumerate(sorted_providers, 1):
        provider["rank"] = i

        # Calculate savings vs highest cost option
        if sort_by == "your_cost" and sorted_providers:
            highest_cost = max(p["your_cost"] for p in provider_estimates)
            provider["savings_vs_highest"] = highest_cost - provider["your_cost"]

    return sorted_providers


def calculate_insurance_value(procedures: List[Dict[str, Any]], insurance_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate the value insurance provides

    Shows how much insurance saves vs paying full price

    Args:
        procedures: List of procedures
        insurance_params: Insurance parameters

    Returns:
        Dictionary with value analysis
    """
    total_billed = sum(p.get("price", 0) for p in procedures)

    # Calculate with insurance
    with_insurance = calculate_total_annual_cost(procedures, insurance_params)

    # Calculate without insurance (full price)
    patient_pays_with_insurance = with_insurance["total_patient_cost"]
    patient_pays_without_insurance = total_billed

    savings = patient_pays_without_insurance - patient_pays_with_insurance
    savings_percentage = (savings / patient_pays_without_insurance * 100) if patient_pays_without_insurance > 0 else 0

    return {
        "total_billed": total_billed,
        "patient_pays_with_insurance": patient_pays_with_insurance,
        "patient_pays_without_insurance": patient_pays_without_insurance,
        "insurance_saves": savings,
        "savings_percentage": round(savings_percentage, 1),
        "insurance_pays": with_insurance["total_insurance_pays"]
    }


def estimate_with_negotiated_rate(billed_amount: float, insurance_type: str = "ppo") -> float:
    """
    Estimate negotiated insurance rate

    Insurance companies negotiate lower rates than billed charges
    This provides a rough estimate of what insurance actually pays

    Args:
        billed_amount: Hospital's billed charge
        insurance_type: Type of insurance (ppo, hmo, medicare, medicaid)

    Returns:
        Estimated negotiated rate
    """
    # Typical discount percentages by insurance type
    discount_rates = {
        "ppo": 0.50,  # PPO typically pays 50% of billed charges
        "hmo": 0.45,  # HMO negotiates even lower
        "medicare": 0.35,  # Medicare pays roughly 35% of billed charges
        "medicaid": 0.30,  # Medicaid pays the least
        "uninsured": 1.00   # Uninsured pays full price (or negotiates themselves)
    }

    rate = discount_rates.get(insurance_type.lower(), 0.50)
    negotiated_amount = billed_amount * rate

    return round(negotiated_amount, 2)


def calculate_monthly_cost_estimate(annual_procedures: List[Dict[str, Any]], insurance_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Estimate monthly healthcare costs including premiums

    Args:
        annual_procedures: Expected procedures for the year
        insurance_params: Insurance parameters including 'monthly_premium' if available

    Returns:
        Monthly cost breakdown
    """
    # Calculate annual out-of-pocket for procedures
    annual_costs = calculate_total_annual_cost(annual_procedures, insurance_params)

    # Get monthly premium (if provided)
    monthly_premium = insurance_params.get("monthly_premium", 0)
    annual_premium = monthly_premium * 12

    # Calculate total annual healthcare spending
    total_annual_spending = annual_premium + annual_costs["total_patient_cost"]

    # Calculate monthly average
    monthly_average = total_annual_spending / 12

    return {
        "monthly_premium": monthly_premium,
        "annual_premium": annual_premium,
        "annual_out_of_pocket": annual_costs["total_patient_cost"],
        "total_annual_spending": total_annual_spending,
        "monthly_average_total": round(monthly_average, 2),
        "breakdown": {
            "premium": monthly_premium,
            "average_procedures": round(annual_costs["total_patient_cost"] / 12, 2)
        }
    }

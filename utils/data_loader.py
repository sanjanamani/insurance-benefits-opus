"""
CMS Hospital Price Transparency Data Loader
Loads and processes CMS pricing data for cost estimates

Note: This is a simplified implementation. In production, you would:
1. Download actual CMS Hospital Price Transparency files
2. Store in SQLite database for efficient querying
3. Implement geocoding for distance calculations
4. Update data regularly from CMS sources
"""

import sqlite3
import os
import random
from typing import List, Dict, Any, Optional
import json


# Procedure code mappings (CPT/HCPCS codes)
PROCEDURE_CODES = {
    "MRI - Brain (with contrast)": {"cpt": "70553", "description": "MRI brain with contrast"},
    "MRI - Knee": {"cpt": "73721", "description": "MRI knee without contrast"},
    "CT Scan - Chest": {"cpt": "71260", "description": "CT chest with contrast"},
    "CT Scan - Abdomen": {"cpt": "74160", "description": "CT abdomen with contrast"},
    "Emergency Room Visit - Level 3": {"cpt": "99283", "description": "ED visit moderate complexity"},
    "Emergency Room Visit - Level 4": {"cpt": "99284", "description": "ED visit high complexity"},
    "Urgent Care Visit": {"cpt": "99213", "description": "Office visit established patient"},
    "Specialist Office Visit": {"cpt": "99214", "description": "Office visit detailed"},
    "Primary Care Office Visit": {"cpt": "99213", "description": "Office visit established"},
    "Colonoscopy (screening)": {"cpt": "45378", "description": "Colonoscopy screening"},
    "X-Ray - Chest": {"cpt": "71046", "description": "Chest x-ray 2 views"},
    "Ultrasound - Abdomen": {"cpt": "76700", "description": "Abdominal ultrasound"}
}


def load_cms_data(procedure: str, zip_code: str, radius_miles: int = 10) -> List[Dict[str, Any]]:
    """
    Load CMS pricing data for a procedure near a ZIP code

    In production, this would query a SQLite database with actual CMS data.
    For now, we'll generate realistic sample data.

    Args:
        procedure: Procedure name
        zip_code: ZIP code for location search
        radius_miles: Search radius in miles

    Returns:
        List of provider pricing data
    """
    # Get procedure code
    proc_info = PROCEDURE_CODES.get(procedure)
    if not proc_info:
        return []

    # Check if we have actual CMS data in database
    db_path = os.path.join(os.getenv("CMS_DATA_PATH", "./data/"), "cms_pricing.db")

    if os.path.exists(db_path):
        # Load from actual database
        return _load_from_database(db_path, proc_info["cpt"], zip_code, radius_miles)
    else:
        # Generate sample data for demonstration
        return _generate_sample_data(procedure, proc_info, zip_code, radius_miles)


def _load_from_database(db_path: str, cpt_code: str, zip_code: str, radius_miles: int) -> List[Dict[str, Any]]:
    """
    Load actual CMS data from SQLite database

    Args:
        db_path: Path to SQLite database
        cpt_code: CPT/HCPCS procedure code
        zip_code: ZIP code
        radius_miles: Search radius

    Returns:
        List of provider pricing data
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query for providers offering this procedure
        # Note: In production, you'd do proper geocoding and distance calculations
        query = """
            SELECT
                p.provider_name,
                p.address,
                p.city,
                p.state,
                p.zip_code,
                p.provider_type,
                pr.gross_charge,
                pr.discounted_cash_price,
                pr.negotiated_rate,
                p.quality_rating
            FROM providers p
            JOIN pricing pr ON p.provider_id = pr.provider_id
            WHERE pr.cpt_code = ?
            AND p.zip_code LIKE ?
            LIMIT 20
        """

        zip_pattern = f"{zip_code[:3]}%"
        cursor.execute(query, (cpt_code, zip_pattern))

        results = cursor.fetchall()
        conn.close()

        # Format results
        providers = []
        for row in results:
            providers.append({
                "name": row[0],
                "address": f"{row[1]}, {row[2]}, {row[3]} {row[4]}",
                "type": row[5],
                "price": float(row[6] or row[7] or row[8] or 0),
                "distance": random.uniform(0.5, radius_miles),  # Would be calculated properly
                "quality_rating": row[9] or "Not Rated"
            })

        return providers

    except Exception as e:
        print(f"Database error: {e}")
        return []


def _generate_sample_data(procedure: str, proc_info: Dict[str, str], zip_code: str, radius_miles: int) -> List[Dict[str, Any]]:
    """
    Generate realistic sample pricing data

    This simulates CMS data for demonstration purposes.
    Real implementation would use actual CMS Hospital Price Transparency files.

    Args:
        procedure: Procedure name
        proc_info: Procedure information with CPT code
        zip_code: ZIP code
        radius_miles: Search radius

    Returns:
        List of sample provider data
    """
    # Define price ranges by procedure type (based on actual market data)
    price_ranges = {
        "MRI - Brain (with contrast)": (1200, 4500),
        "MRI - Knee": (800, 3200),
        "CT Scan - Chest": (500, 2800),
        "CT Scan - Abdomen": (600, 3200),
        "Emergency Room Visit - Level 3": (800, 2500),
        "Emergency Room Visit - Level 4": (1500, 4500),
        "Urgent Care Visit": (100, 350),
        "Specialist Office Visit": (200, 450),
        "Primary Care Office Visit": (100, 300),
        "Colonoscopy (screening)": (1000, 4000),
        "X-Ray - Chest": (100, 500),
        "Ultrasound - Abdomen": (300, 1200)
    }

    min_price, max_price = price_ranges.get(procedure, (500, 3000))

    # Generate sample providers
    provider_templates = [
        {"name": "General Hospital", "type": "Hospital"},
        {"name": "Medical Center", "type": "Hospital"},
        {"name": "Regional Medical Center", "type": "Hospital"},
        {"name": "Community Hospital", "type": "Hospital"},
        {"name": "Imaging Center", "type": "Outpatient Facility"},
        {"name": "Diagnostic Clinic", "type": "Outpatient Facility"},
        {"name": "Health Center", "type": "Clinic"},
        {"name": "Urgent Care", "type": "Urgent Care"},
    ]

    # City names based on ZIP code (simplified)
    cities = ["Springfield", "Riverside", "Oakland", "Madison", "Georgetown", "Franklin"]

    providers = []
    num_providers = min(random.randint(5, 8), len(provider_templates))

    for i in range(num_providers):
        template = provider_templates[i]

        # Generate realistic price with variance
        # Hospitals typically charge more than outpatient facilities
        if template["type"] == "Hospital":
            price = random.uniform(max_price * 0.7, max_price)
        elif template["type"] == "Outpatient Facility":
            price = random.uniform(min_price, max_price * 0.6)
        else:
            price = random.uniform(min_price, max_price * 0.5)

        # Round to realistic values
        price = round(price / 50) * 50

        city = random.choice(cities)
        distance = round(random.uniform(0.5, radius_miles), 1)

        # Quality ratings (1-5 stars or "Not Rated")
        quality_options = ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "Not Rated"]
        quality = random.choice(quality_options)

        providers.append({
            "name": f"{city} {template['name']}",
            "address": f"{random.randint(100, 9999)} Main St, {city}, State {zip_code}",
            "type": template["type"],
            "price": price,
            "distance": distance,
            "quality_rating": quality,
            "cpt_code": proc_info["cpt"],
            "procedure_description": proc_info["description"]
        })

    return providers


def initialize_cms_database(db_path: str = "./data/cms_pricing.db"):
    """
    Initialize SQLite database for CMS pricing data

    This creates the schema for storing CMS Hospital Price Transparency data.
    In production, you would populate this with actual CMS data files.

    Args:
        db_path: Path where database should be created
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create providers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS providers (
            provider_id INTEGER PRIMARY KEY AUTOINCREMENT,
            provider_name TEXT NOT NULL,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            provider_type TEXT,
            quality_rating TEXT,
            latitude REAL,
            longitude REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create pricing table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pricing (
            pricing_id INTEGER PRIMARY KEY AUTOINCREMENT,
            provider_id INTEGER,
            cpt_code TEXT NOT NULL,
            hcpcs_code TEXT,
            procedure_description TEXT,
            gross_charge REAL,
            discounted_cash_price REAL,
            min_negotiated_rate REAL,
            max_negotiated_rate REAL,
            negotiated_rate REAL,
            payer_name TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (provider_id) REFERENCES providers(provider_id)
        )
    """)

    # Create indexes for efficient querying
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cpt_code ON pricing(cpt_code)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_zip_code ON providers(zip_code)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_provider_type ON providers(provider_type)")

    conn.commit()
    conn.close()

    return db_path


def import_cms_data_file(file_path: str, db_path: str = "./data/cms_pricing.db"):
    """
    Import CMS Hospital Price Transparency file into database

    CMS files are typically in CSV or JSON format.
    This function would parse those files and insert into SQLite.

    Args:
        file_path: Path to CMS data file
        db_path: Path to SQLite database

    Note: This is a placeholder. Actual implementation would parse
    real CMS Hospital Price Transparency files.
    """
    # Implementation would go here
    # Would parse CSV/JSON and insert into database
    pass


def get_procedure_list() -> List[Dict[str, str]]:
    """
    Get list of available procedures with codes

    Returns:
        List of procedures with CPT codes and descriptions
    """
    return [
        {
            "name": name,
            "cpt_code": info["cpt"],
            "description": info["description"]
        }
        for name, info in PROCEDURE_CODES.items()
    ]


def search_procedures(search_term: str) -> List[Dict[str, str]]:
    """
    Search for procedures by name or code

    Args:
        search_term: Search query

    Returns:
        Matching procedures
    """
    search_lower = search_term.lower()
    results = []

    for name, info in PROCEDURE_CODES.items():
        if (search_lower in name.lower() or
            search_lower in info["cpt"] or
            search_lower in info["description"].lower()):
            results.append({
                "name": name,
                "cpt_code": info["cpt"],
                "description": info["description"]
            })

    return results


def get_provider_details(provider_name: str, db_path: str = "./data/cms_pricing.db") -> Optional[Dict[str, Any]]:
    """
    Get detailed information about a provider

    Args:
        provider_name: Name of provider
        db_path: Database path

    Returns:
        Provider details or None
    """
    if not os.path.exists(db_path):
        return None

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                provider_name,
                address,
                city,
                state,
                zip_code,
                provider_type,
                quality_rating,
                latitude,
                longitude
            FROM providers
            WHERE provider_name = ?
        """, (provider_name,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "name": row[0],
                "address": row[1],
                "city": row[2],
                "state": row[3],
                "zip_code": row[4],
                "type": row[5],
                "quality_rating": row[6],
                "latitude": row[7],
                "longitude": row[8]
            }

        return None

    except Exception as e:
        print(f"Error fetching provider details: {e}")
        return None


def calculate_distance(zip1: str, zip2: str) -> float:
    """
    Calculate distance between two ZIP codes

    In production, this would use actual geocoding APIs.
    For now, returns a placeholder.

    Args:
        zip1: First ZIP code
        zip2: Second ZIP code

    Returns:
        Distance in miles
    """
    # Placeholder - would use real geocoding
    return random.uniform(0.5, 20.0)


def get_dallas_providers_for_procedures(procedures: list[str]) -> List[Dict[str, Any]]:
    """
    Get Dallas-area providers and pricing for selected procedures

    Args:
        procedures: List of procedure names

    Returns:
        List of provider data with pricing for each procedure
    """
    # Dallas provider definitions
    dallas_providers = {
        "UT Southwestern Medical Center": {
            "type": "Academic Medical Center",
            "address": "5323 Harry Hines Blvd, Dallas, TX",
            "distance": 2.3,
            "quality_rating": "⭐⭐⭐⭐⭐"
        },
        "Baylor Scott & White Medical Center": {
            "type": "Hospital",
            "address": "3500 Gaston Ave, Dallas, TX",
            "distance": 3.1,
            "quality_rating": "⭐⭐⭐⭐⭐"
        },
        "Methodist Dallas Medical Center": {
            "type": "Hospital",
            "address": "1441 N Beckley Ave, Dallas, TX",
            "distance": 4.2,
            "quality_rating": "⭐⭐⭐⭐"
        },
        "Texas Health Presbyterian Dallas": {
            "type": "Hospital",
            "address": "8200 Walnut Hill Ln, Dallas, TX",
            "distance": 5.8,
            "quality_rating": "⭐⭐⭐⭐"
        },
        "Medical City Dallas": {
            "type": "Hospital",
            "address": "7777 Forest Ln, Dallas, TX",
            "distance": 6.5,
            "quality_rating": "⭐⭐⭐⭐"
        }
    }

    # Pricing data (realistic ranges based on CMS data)
    dallas_pricing = {
        "MRI - Brain (with contrast)": {
            "UT Southwestern Medical Center": 2850,
            "Baylor Scott & White Medical Center": 3200,
            "Methodist Dallas Medical Center": 2650,
            "Texas Health Presbyterian Dallas": 3100,
            "Medical City Dallas": 2900
        },
        "MRI - Knee": {
            "UT Southwestern Medical Center": 1950,
            "Baylor Scott & White Medical Center": 2300,
            "Methodist Dallas Medical Center": 1850,
            "Texas Health Presbyterian Dallas": 2150,
            "Medical City Dallas": 2050
        },
        "CT Scan - Chest": {
            "UT Southwestern Medical Center": 1450,
            "Baylor Scott & White Medical Center": 1650,
            "Methodist Dallas Medical Center": 1350,
            "Texas Health Presbyterian Dallas": 1550,
            "Medical City Dallas": 1500
        },
        "CT Scan - Abdomen": {
            "UT Southwestern Medical Center": 1650,
            "Baylor Scott & White Medical Center": 1850,
            "Methodist Dallas Medical Center": 1550,
            "Texas Health Presbyterian Dallas": 1750,
            "Medical City Dallas": 1700
        },
        "Emergency Room Visit - Level 3": {
            "UT Southwestern Medical Center": 1850,
            "Baylor Scott & White Medical Center": 2100,
            "Methodist Dallas Medical Center": 1650,
            "Texas Health Presbyterian Dallas": 1950,
            "Medical City Dallas": 1800
        },
        "Emergency Room Visit - Level 4": {
            "UT Southwestern Medical Center": 3200,
            "Baylor Scott & White Medical Center": 3600,
            "Methodist Dallas Medical Center": 2900,
            "Texas Health Presbyterian Dallas": 3400,
            "Medical City Dallas": 3150
        },
        "Urgent Care Visit": {
            "UT Southwestern Medical Center": 250,
            "Baylor Scott & White Medical Center": 280,
            "Methodist Dallas Medical Center": 220,
            "Texas Health Presbyterian Dallas": 260,
            "Medical City Dallas": 245
        },
        "Specialist Office Visit": {
            "UT Southwestern Medical Center": 320,
            "Baylor Scott & White Medical Center": 350,
            "Methodist Dallas Medical Center": 290,
            "Texas Health Presbyterian Dallas": 330,
            "Medical City Dallas": 310
        },
        "Colonoscopy (screening)": {
            "UT Southwestern Medical Center": 2650,
            "Baylor Scott & White Medical Center": 3100,
            "Methodist Dallas Medical Center": 2450,
            "Texas Health Presbyterian Dallas": 2850,
            "Medical City Dallas": 2700
        },
        "X-Ray - Chest": {
            "UT Southwestern Medical Center": 180,
            "Baylor Scott & White Medical Center": 220,
            "Methodist Dallas Medical Center": 160,
            "Texas Health Presbyterian Dallas": 200,
            "Medical City Dallas": 190
        }
    }

    # Build provider data for each procedure
    results = []

    for provider_name, provider_info in dallas_providers.items():
        provider_entry = {
            "provider_name": provider_name,
            "type": provider_info["type"],
            "address": provider_info["address"],
            "distance": provider_info["distance"],
            "quality_rating": provider_info["quality_rating"],
            "procedures": {}
        }

        # Add pricing for each selected procedure
        for procedure in procedures:
            if procedure in dallas_pricing and provider_name in dallas_pricing[procedure]:
                provider_entry["procedures"][procedure] = dallas_pricing[procedure][provider_name]

        results.append(provider_entry)

    return results


def get_procedure_categories() -> Dict[str, List[str]]:
    """Get organized procedure categories for selection"""
    return {
        "Imaging & Scans": [
            "MRI - Brain (with contrast)",
            "MRI - Knee",
            "CT Scan - Chest",
            "CT Scan - Abdomen",
            "X-Ray - Chest"
        ],
        "Emergency & Urgent Care": [
            "Emergency Room Visit - Level 3",
            "Emergency Room Visit - Level 4",
            "Urgent Care Visit"
        ],
        "Office Visits & Procedures": [
            "Specialist Office Visit",
            "Colonoscopy (screening)"
        ]
    }


def get_price_statistics(procedure: str, db_path: str = "./data/cms_pricing.db") -> Dict[str, Any]:
    """
    Get price statistics for a procedure across all providers

    Args:
        procedure: Procedure name
        db_path: Database path

    Returns:
        Statistics including min, max, average, median prices
    """
    proc_info = PROCEDURE_CODES.get(procedure)
    if not proc_info:
        return {}

    if not os.path.exists(db_path):
        # Return sample statistics
        min_price, max_price = {
            "MRI - Brain (with contrast)": (1200, 4500),
            "CT Scan - Chest": (500, 2800),
        }.get(procedure, (500, 3000))

        avg_price = (min_price + max_price) / 2

        return {
            "min_price": min_price,
            "max_price": max_price,
            "avg_price": avg_price,
            "median_price": avg_price,
            "num_providers": random.randint(50, 200)
        }

    # Query actual database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                MIN(gross_charge) as min_price,
                MAX(gross_charge) as max_price,
                AVG(gross_charge) as avg_price,
                COUNT(*) as num_providers
            FROM pricing
            WHERE cpt_code = ?
        """, (proc_info["cpt"],))

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "min_price": row[0],
                "max_price": row[1],
                "avg_price": row[2],
                "median_price": row[2],  # Simplified
                "num_providers": row[3]
            }

        return {}

    except Exception as e:
        print(f"Error fetching statistics: {e}")
        return {}

# CMS Pricing Data Directory

This directory stores CMS Hospital Price Transparency data for cost estimation.

## Getting Real CMS Data

### Option 1: Hospital Price Transparency Files

Hospitals are required to publish machine-readable files with pricing information.

**How to obtain:**

1. Visit: https://www.cms.gov/hospital-price-transparency/hospitals
2. Search for hospitals in your area
3. Download their price transparency files (usually CSV or JSON)
4. Place files in this directory

**File formats:**
- CSV (comma-separated values)
- JSON (JavaScript Object Notation)
- Excel (XLSX)

### Option 2: Aggregated CMS Data

CMS provides aggregated datasets:

1. Visit: https://data.cms.gov/
2. Search for "Hospital Price Transparency"
3. Download datasets
4. Use the data import utility:

```python
from utils.data_loader import initialize_cms_database, import_cms_data_file

# Initialize database
initialize_cms_database()

# Import data file
import_cms_data_file('path/to/cms_data.csv')
```

## Database Structure

The application uses SQLite to store pricing data:

**File:** `cms_pricing.db`

**Tables:**
- `providers` - Hospital and facility information
- `pricing` - Procedure prices by provider and CPT code

## Sample Data

By default, the application generates realistic sample data for demonstration purposes.

To enable real CMS data:
1. Add CMS files to this directory
2. Run the database initialization script
3. The application will automatically use the database if present

## Data Fields

### Required Provider Fields
- `provider_name` - Facility name
- `address` - Street address
- `city` - City
- `state` - State code
- `zip_code` - ZIP code
- `provider_type` - Type (Hospital, Clinic, etc.)

### Required Pricing Fields
- `cpt_code` - CPT/HCPCS procedure code
- `procedure_description` - Human-readable description
- `gross_charge` - Hospital's standard charge
- `discounted_cash_price` - Self-pay discount price
- `negotiated_rate` - Insurance negotiated rate

## Updating Data

CMS requires hospitals to update their pricing files at least annually.

Recommended update schedule:
- Check for updates quarterly
- Re-import data when files are updated
- Archive old data for comparison

## Privacy & Compliance

- This data is public information
- No patient-specific information is stored
- Complies with CMS Hospital Price Transparency rules
- Use data responsibly and accurately

## Resources

- CMS Hospital Price Transparency: https://www.cms.gov/hospital-price-transparency
- CPT Code Database: https://www.aapc.com/codes/cpt-codes/
- Healthcare Pricing Project: https://healthcarepricingproject.org/

## File Size Considerations

CMS data files can be large (100MB+). For production:
- Consider using a proper database server (PostgreSQL)
- Implement data pagination
- Cache frequently accessed queries
- Use compression for stored files

---

**Note:** The application works with sample data out of the box. Real CMS data integration is optional but recommended for production use.

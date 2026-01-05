# Healthcare Cost Transparency Platform

A Streamlit-based web application that helps patients understand their insurance benefits and estimate healthcare costs using real pricing data.

## Features

### 1. Insurance Benefits Decoder
- Upload insurance cards (PDF/images) or policy documents
- AI-powered extraction of key coverage details using Claude API
- Plain English explanations of complex insurance terms
- Interactive Q&A about your coverage
- Visual progress tracking for deductibles and out-of-pocket maximums

**Key Details Extracted:**
- Plan name and type
- Deductible amounts (individual/family)
- Copay amounts (primary care, specialist, ER, urgent care)
- Coinsurance percentages
- Out-of-pocket maximum
- In-network vs out-of-network coverage
- Pharmacy benefits

### 2. Personalized Cost Estimator
- Select common medical procedures (MRI, CT scan, ER visits, etc.)
- View real pricing data from CMS Hospital Price Transparency files
- Calculate actual out-of-pocket costs based on YOUR insurance
- Side-by-side provider comparison
- Surprise billing risk assessment
- Visual cost breakdowns and charts

**Procedures Supported:**
- MRI scans (brain, knee, etc.)
- CT scans (chest, abdomen)
- Emergency room visits
- Urgent care visits
- Office visits (primary care, specialist)
- Colonoscopy
- X-rays and ultrasounds
- And more...

## Tech Stack

- **Frontend:** Streamlit
- **AI/ML:** Anthropic Claude API (Opus 4.5)
- **Data Storage:** SQLite
- **Visualization:** Plotly
- **Document Processing:** PyPDF2, Pillow, pytesseract
- **Environment:** python-dotenv

## Installation

### Prerequisites
- Python 3.9 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd insurance-benefits-opus
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
```

4. Edit `.env` and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

5. Run the application:
```bash
streamlit run app.py
```

6. Open your browser to `http://localhost:8501`

## Usage

### Using the Insurance Benefits Decoder

1. Navigate to "Insurance Benefits Decoder" in the sidebar
2. Upload your insurance card (front/back) or policy document
3. Click "Analyze Document"
4. Review the extracted coverage details
5. Ask questions about your coverage in the chat interface

### Using the Cost Estimator

1. Navigate to "Cost Estimator" in the sidebar
2. Enter your insurance information:
   - Annual deductible
   - Amount already paid toward deductible
   - Coinsurance percentage
   - Out-of-pocket maximum
   - Amount paid toward OOP max
3. Select a medical procedure
4. Enter your ZIP code and search radius
5. Click "Get Cost Estimates"
6. Review provider comparisons and cost breakdowns

## Project Structure

```
insurance-benefits-opus/
├── app.py                      # Main Streamlit application
├── utils/
│   ├── __init__.py
│   ├── claude_parser.py        # Document extraction with Claude API
│   ├── cost_calculator.py      # Insurance cost calculation logic
│   └── data_loader.py          # CMS data loading and processing
├── data/                       # CMS pricing data storage
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## Data Sources

### CMS Hospital Price Transparency Data

The Cost Estimator uses data from the [CMS Hospital Price Transparency](https://www.cms.gov/hospital-price-transparency) initiative, which requires hospitals to publish their prices for common procedures.

**Note:** Currently, the application generates realistic sample data for demonstration. To use real CMS data:

1. Download CMS Hospital Price Transparency files
2. Run the database initialization:
```python
from utils.data_loader import initialize_cms_database
initialize_cms_database()
```
3. Import CMS data files into the database

## How It Works

### Insurance Benefits Decoder

1. **Document Upload:** Users upload insurance cards or policy PDFs
2. **Text Extraction:** PyPDF2 extracts text from PDFs; images are processed with Claude Vision
3. **AI Analysis:** Claude API analyzes the document and extracts key insurance details
4. **Structured Output:** Data is parsed into structured format and displayed
5. **Q&A Interface:** Users can ask follow-up questions about their coverage

### Cost Estimator

1. **Insurance Input:** User enters their insurance parameters
2. **Procedure Selection:** User selects a medical procedure
3. **Data Retrieval:** System loads CMS pricing data for local providers
4. **Cost Calculation:** Applies insurance math (deductible → coinsurance → OOP max)
5. **Risk Assessment:** Evaluates surprise billing risk factors
6. **Comparison Display:** Shows side-by-side provider comparison with costs

### Insurance Cost Calculation Logic

The system implements the standard insurance payment waterfall:

1. **Deductible Phase:** Patient pays full cost until deductible is met
2. **Coinsurance Phase:** Patient pays percentage (e.g., 20%) after deductible
3. **Out-of-Pocket Maximum:** Once reached, insurance pays 100%

Example for $2,000 MRI:
- Deductible: $1,500 (with $500 already paid)
- Coinsurance: 20%
- Remaining deductible: $1,000

Calculation:
1. $1,000 goes to remaining deductible
2. $1,000 remaining × 20% coinsurance = $200
3. **Patient pays: $1,200**
4. **Insurance pays: $800**

## API Usage

### Claude API

The application uses Claude for:
- **Document Analysis:** Extracting insurance details from PDFs and images
- **Vision Processing:** Reading insurance cards via Claude's vision capabilities
- **Q&A:** Answering user questions about coverage

**Model:** Claude Opus 4.5 (`claude-opus-4-5-20251101`)

**API Calls:**
- Document parsing: ~1 call per document
- Q&A: 1 call per question
- Typical cost: $0.01-0.05 per document analysis

## Security & Privacy

- API keys stored in `.env` file (never committed to git)
- Documents processed in-memory, not stored permanently
- No user data stored or transmitted except to Claude API
- Follow HIPAA guidelines if deploying for production use

## Limitations & Disclaimers

⚠️ **Important Disclaimers:**

1. **Not Medical or Legal Advice:** This tool provides estimates only
2. **Verify with Provider:** Always confirm costs with healthcare providers
3. **Sample Data:** Default CMS data is simulated for demonstration
4. **Surprise Billing:** Risk assessment is an estimate, not a guarantee
5. **Coverage Variations:** Actual coverage may differ from extracted information
6. **For Educational Use:** Not intended for production medical use without proper review

## Future Enhancements

- [ ] Real-time CMS data integration
- [ ] Interactive map view with provider locations
- [ ] Export cost estimates to PDF
- [ ] Multi-plan comparison
- [ ] HSA/FSA calculator
- [ ] Historical cost tracking
- [ ] Provider quality ratings integration
- [ ] Mobile app version
- [ ] Multi-language support

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues or questions:
- Create a GitHub issue
- Check documentation at [link]
- Contact: [your-email]

## Acknowledgments

- **Anthropic** for Claude API
- **CMS** for Hospital Price Transparency initiative
- **Streamlit** for the excellent framework
- **Healthcare pricing transparency advocates** for making data accessible

## Version

Current version: 1.0.0 (Initial Release)

---

**Made with ❤️ to help patients navigate healthcare costs**

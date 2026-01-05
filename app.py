"""
Healthcare Cost Transparency Platform
Main Streamlit application with two core features:
1. Insurance Benefits Decoder
2. Personalized Cost Estimator
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Healthcare Cost Transparency Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and better UI
st.markdown("""
    <style>
    /* Main headers */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4da6ff;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #b0b0b0;
        margin-bottom: 2rem;
    }

    /* Dark theme cards */
    .dark-card {
        background: linear-gradient(135deg, #1e2530 0%, #252d3d 100%);
        color: #e0e0e0;
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin-bottom: 1rem;
        border: 1px solid #3a4556;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }

    .info-card {
        background: linear-gradient(135deg, #2a3142 0%, #323b4f 100%);
        color: #e8e8e8;
        padding: 1.2rem;
        border-radius: 0.5rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid #4da6ff;
    }

    .metric-card {
        background: #252d3d;
        color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        border: 1px solid #3a4556;
    }

    .metric-label {
        color: #9ca3af;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 0.3rem;
    }

    .metric-value {
        color: #4da6ff;
        font-size: 1.8rem;
        font-weight: bold;
    }

    /* Coverage sections */
    .coverage-section {
        background: #1e2530;
        color: #e0e0e0;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 3px solid #10b981;
    }

    .coverage-item {
        color: #d1d5db;
        padding: 0.3rem 0;
        border-bottom: 1px solid #374151;
    }

    .coverage-item:last-child {
        border-bottom: none;
    }

    /* Tables */
    .stDataFrame {
        background-color: #1e2530 !important;
    }

    /* Better contrast for text */
    .element-container {
        color: #e0e0e0;
    }

    /* Demo badge */
    .demo-badge {
        background: linear-gradient(90deg, #f59e0b 0%, #ef4444 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        display: inline-block;
        font-weight: bold;
        margin: 0.5rem 0;
    }

    /* Success/Warning alerts */
    .success-alert {
        background: #065f46;
        color: #d1fae5;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #10b981;
    }

    .warning-alert {
        background: #78350f;
        color: #fef3c7;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f59e0b;
    }

    /* Procedure selection cards */
    .procedure-card {
        background: #252d3d;
        padding: 0.8rem;
        border-radius: 0.5rem;
        margin: 0.3rem 0;
        border: 1px solid #3a4556;
        cursor: pointer;
        transition: all 0.2s;
    }

    .procedure-card:hover {
        background: #2d3548;
        border-color: #4da6ff;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    """Main application entry point"""

    # Initialize session state for insurance details
    if 'insurance_data' not in st.session_state:
        st.session_state.insurance_data = None
    if 'parsed_coverage' not in st.session_state:
        st.session_state.parsed_coverage = None
    if 'demo_mode' not in st.session_state:
        st.session_state.demo_mode = False

    # Sidebar navigation
    st.sidebar.title("🏥 Healthcare Transparency")
    st.sidebar.markdown("---")

    # Demo mode toggle
    if st.sidebar.button("🎯 Try Demo Mode", use_container_width=True):
        st.session_state.demo_mode = True
        load_demo_data()
        st.rerun()

    if st.session_state.demo_mode:
        st.sidebar.markdown('<div class="demo-badge">DEMO MODE ACTIVE</div>', unsafe_allow_html=True)
        if st.sidebar.button("Exit Demo", use_container_width=True):
            st.session_state.demo_mode = False
            st.session_state.insurance_data = None
            st.session_state.parsed_coverage = None
            st.rerun()

    # Feature selection
    feature = st.sidebar.radio(
        "Select Feature:",
        ["🏠 Home", "📋 Insurance Benefits Decoder", "💰 Cost Estimator"],
        index=0
    )

    st.sidebar.markdown("---")
    st.sidebar.info(
        "**About This Platform**\n\n"
        "This tool helps you:\n"
        "- Understand your insurance coverage\n"
        "- Estimate healthcare costs\n"
        "- Compare provider prices\n"
        "- Avoid surprise medical bills"
    )

    # Show insurance status in sidebar
    if st.session_state.parsed_coverage:
        st.sidebar.markdown("---")
        st.sidebar.success(
            f"**Insurance Loaded**\n\n"
            f"Plan: {st.session_state.parsed_coverage.get('plan_name', 'Unknown')}\n\n"
            f"Deductible: {st.session_state.parsed_coverage.get('deductible', 'N/A')}"
        )

    # Route to selected feature
    if feature == "🏠 Home":
        show_home()
    elif feature == "📋 Insurance Benefits Decoder":
        show_insurance_decoder()
    elif feature == "💰 Cost Estimator":
        show_cost_estimator()

def load_demo_data():
    """Load demo insurance and provider data"""
    st.session_state.parsed_coverage = {
        "success": True,
        "plan_name": "Blue Cross Blue Shield - PPO Plus",
        "deductible": "$2,000",
        "deductible_value": 2000,
        "oop_max": "$6,500",
        "oop_max_value": 6500,
        "copay_primary": "$30",
        "copay_specialist": "$60",
        "copay_er": "$350",
        "copay_urgent_care": "$75",
        "coinsurance": "20%",
        "coinsurance_value": 0.20,
        "network_type": "PPO",
        "covered_services": [
            "Preventive care (100% covered)",
            "Primary care visits",
            "Specialist consultations",
            "Emergency services",
            "Urgent care",
            "Lab tests and imaging (MRI, CT, X-ray)",
            "Outpatient surgery",
            "Physical therapy (20 visits/year)",
            "Mental health services"
        ],
        "requires_prior_auth": [
            "MRI and advanced imaging",
            "Outpatient surgery",
            "Durable medical equipment",
            "Home health care"
        ],
        "not_covered": [
            "Cosmetic procedures",
            "Experimental treatments",
            "Alternative medicine (acupuncture)"
        ],
        "in_network_vs_out": {
            "in_network": "Deductible: $2,000 | Coinsurance: 20% | OOP Max: $6,500",
            "out_of_network": "Deductible: $4,000 | Coinsurance: 40% | OOP Max: $13,000"
        },
        "pharmacy_benefits": "Generic: $10 | Preferred Brand: $40 | Non-Preferred: $70",
        "plain_english_summary": """
**Your Coverage at a Glance:**

This is a PPO (Preferred Provider Organization) plan, which means you have flexibility to see specialists without referrals, but you'll save money using in-network providers.

**How Your Coverage Works:**
1. You pay the first $2,000 of covered services (your deductible)
2. After that, you pay 20% of costs (coinsurance) and insurance pays 80%
3. Once you've paid $6,500 total out-of-pocket, insurance covers 100%

**Office Visits:**
- Primary care: $30 copay (no deductible required)
- Specialists: $60 copay (no deductible required)
- Urgent care: $75 copay
- ER: $350 copay (waived if admitted)

**Important Notes:**
- Preventive care is FREE (annual checkups, vaccines, screenings)
- Some services need prior authorization (pre-approval)
- Out-of-network care costs significantly more
        """
    }

    st.session_state.insurance_data = {
        "deductible_total": 2000,
        "deductible_met": 500,  # Already paid $500
        "coinsurance": 0.20,
        "oop_max": 6500,
        "oop_met": 800,  # Already paid $800 total
        "network": "in_network"
    }

def show_home():
    """Display home page with platform overview"""

    st.markdown('<div class="main-header">Healthcare Cost Transparency Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Empowering patients with clear healthcare cost information</div>', unsafe_allow_html=True)

    # Introduction
    st.markdown("""
    ## Welcome! 👋

    Healthcare costs can be confusing and overwhelming. This platform helps you:
    - **Decode** your insurance benefits in plain English
    - **Estimate** actual costs for common medical procedures
    - **Compare** prices across different healthcare providers
    - **Understand** your out-of-pocket expenses before you receive care
    """)

    # Feature cards
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📋 Insurance Benefits Decoder")
        st.markdown("""
        <div class="feature-card">
        <strong>What it does:</strong>
        <ul>
        <li>Upload your insurance card or policy document</li>
        <li>Automatically extracts key coverage details</li>
        <li>Explains benefits in plain English</li>
        <li>Ask questions about your coverage</li>
        </ul>
        <strong>You'll learn:</strong> Deductibles, copays, coinsurance, out-of-pocket maximums, and network coverage
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 💰 Personalized Cost Estimator")
        st.markdown("""
        <div class="feature-card">
        <strong>What it does:</strong>
        <ul>
        <li>Select common medical procedures</li>
        <li>View real pricing data from local providers</li>
        <li>Calculate your actual out-of-pocket costs</li>
        <li>Compare facilities side-by-side</li>
        </ul>
        <strong>You'll learn:</strong> Estimated costs based on YOUR insurance and how much you've paid toward your deductible
        </div>
        """, unsafe_allow_html=True)

    # Getting started
    st.markdown("---")
    st.markdown("## 🚀 Getting Started")
    st.markdown("""
    1. **Start with the Insurance Benefits Decoder** (left sidebar) to understand your coverage
    2. **Then use the Cost Estimator** to see what procedures will actually cost you
    3. **Make informed decisions** about your healthcare
    """)

    # API key check
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        st.warning("⚠️ **Setup Required**: Please configure your Anthropic API key in the `.env` file to use the Insurance Benefits Decoder feature.")

def show_insurance_decoder():
    """Display Insurance Benefits Decoder feature with multi-file upload"""

    st.title("📋 Insurance Benefits Decoder")
    st.markdown("Upload multiple insurance documents to get a comprehensive view of your coverage.")

    # Check if already loaded (from demo or previous upload)
    if st.session_state.parsed_coverage and not st.session_state.demo_mode:
        display_parsed_coverage(st.session_state.parsed_coverage)
        return

    # Demo mode: show demo data
    if st.session_state.demo_mode and st.session_state.parsed_coverage:
        st.info("🎯 **Demo Mode**: Showing sample insurance coverage")
        display_parsed_coverage(st.session_state.parsed_coverage)
        return

    # Check API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        st.markdown('<div class="warning-alert">⚠️ <strong>API Key Required</strong><br>Please set your Anthropic API key in the <code>.env</code> file to use this feature.</div>', unsafe_allow_html=True)
        st.code("ANTHROPIC_API_KEY=your_actual_api_key", language="bash")

        # Still allow demo mode without API key
        if st.button("🎯 Try Demo Instead", type="primary"):
            st.session_state.demo_mode = True
            load_demo_data()
            st.rerun()
        return

    # Multi-file upload section
    st.markdown("### 📤 Upload Your Insurance Documents")

    col1, col2 = st.columns([2, 1])

    with col1:
        uploaded_files = st.file_uploader(
            "Choose one or more files (PDF or Images)",
            type=["pdf", "png", "jpg", "jpeg"],
            accept_multiple_files=True,
            help="Upload your insurance card (front & back), policy document, or benefits summary"
        )

    with col2:
        st.markdown("""
        <div class="info-card">
        <strong>📁 Accepted:</strong><br>
        • PDF documents<br>
        • Images (PNG, JPG)<br><br>
        <strong>💡 Tip:</strong><br>
        Upload multiple documents for more complete coverage information!
        </div>
        """, unsafe_allow_html=True)

    if uploaded_files:
        # Display uploaded files
        st.markdown(f'<div class="success-alert">✅ Uploaded {len(uploaded_files)} file(s)</div>', unsafe_allow_html=True)
        for file in uploaded_files:
            st.text(f"• {file.name}")

        # Parse button
        if st.button("🔍 Analyze Documents", type="primary", use_container_width=True):
            with st.spinner("🤖 Analyzing your insurance documents with AI..."):
                from utils.claude_parser import parse_insurance_document, merge_parsed_results

                # Parse all documents
                results = []
                for uploaded_file in uploaded_files:
                    result = parse_insurance_document(uploaded_file)
                    if result.get("success"):
                        results.append(result)

                if results:
                    # Merge results from multiple documents
                    merged_result = merge_parsed_results(results) if len(results) > 1 else results[0]

                    # Save to session state
                    st.session_state.parsed_coverage = merged_result

                    # Extract numeric values for cost estimator
                    st.session_state.insurance_data = extract_insurance_params(merged_result)

                    # Display results
                    st.success("✅ Analysis complete! Your coverage details have been saved.")
                    st.rerun()
                else:
                    st.error("❌ Could not extract information from the uploaded documents. Please try different files or use Demo Mode.")

    else:
        # Show example/instructions
        st.markdown("""
        <div class="dark-card">
        <h3>👆 Upload documents to get started</h3>

        <p><strong>What we'll extract:</strong></p>
        <ul>
            <li>Plan name and network type</li>
            <li>Deductible amounts (individual/family)</li>
            <li>Copay amounts (primary care, specialist, ER, urgent care)</li>
            <li>Coinsurance percentages</li>
            <li>Out-of-pocket maximum</li>
            <li>In-network vs out-of-network coverage</li>
            <li>Covered services and exclusions</li>
            <li>Prior authorization requirements</li>
            <li>Pharmacy benefits</li>
        </ul>

        <p><strong>Pro tip:</strong> Upload both front and back of your insurance card plus any policy documents for the most comprehensive analysis!</p>
        </div>
        """, unsafe_allow_html=True)

def display_parsed_coverage(coverage):
    """Display parsed insurance coverage with dark theme cards"""

    st.markdown("### 📊 Your Coverage Summary")

    # Key metrics in custom cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Plan Name</div>
            <div class="metric-value" style="font-size: 1.2rem; color: #10b981;">{coverage.get('plan_name', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Deductible</div>
            <div class="metric-value">{coverage.get('deductible', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Out-of-Pocket Max</div>
            <div class="metric-value">{coverage.get('oop_max', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Coinsurance</div>
            <div class="metric-value">{coverage.get('coinsurance', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)

    # Copay information
    st.markdown("### 💳 Copay Amounts")
    copay_col1, copay_col2, copay_col3, copay_col4 = st.columns(4)

    with copay_col1:
        st.markdown(f"""
        <div class="info-card">
        <strong>Primary Care</strong><br>
        <span style="font-size: 1.5rem; color: #4da6ff;">{coverage.get('copay_primary', 'N/A')}</span>
        </div>
        """, unsafe_allow_html=True)

    with copay_col2:
        st.markdown(f"""
        <div class="info-card">
        <strong>Specialist</strong><br>
        <span style="font-size: 1.5rem; color: #4da6ff;">{coverage.get('copay_specialist', 'N/A')}</span>
        </div>
        """, unsafe_allow_html=True)

    with copay_col3:
        st.markdown(f"""
        <div class="info-card">
        <strong>Urgent Care</strong><br>
        <span style="font-size: 1.5rem; color: #4da6ff;">{coverage.get('copay_urgent_care', 'N/A')}</span>
        </div>
        """, unsafe_allow_html=True)

    with copay_col4:
        st.markdown(f"""
        <div class="info-card">
        <strong>Emergency Room</strong><br>
        <span style="font-size: 1.5rem; color: #4da6ff;">{coverage.get('copay_er', 'N/A')}</span>
        </div>
        """, unsafe_allow_html=True)

    # Plain English summary
    st.markdown("### 📖 Coverage Explained")
    st.markdown(f"""
    <div class="dark-card">
    {coverage.get('plain_english_summary', 'No summary available')}
    </div>
    """, unsafe_allow_html=True)

    # Comprehensive breakdown
    st.markdown("### 📋 Detailed Coverage Breakdown")

    detail_col1, detail_col2 = st.columns(2)

    with detail_col1:
        # Covered services
        if coverage.get('covered_services'):
            st.markdown("""
            <div class="coverage-section">
            <h4 style="color: #10b981; margin-top: 0;">✅ Covered Services</h4>
            """, unsafe_allow_html=True)
            for service in coverage.get('covered_services', []):
                st.markdown(f'<div class="coverage-item">• {service}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Prior authorization required
        if coverage.get('requires_prior_auth'):
            st.markdown("""
            <div class="coverage-section" style="border-left-color: #f59e0b;">
            <h4 style="color: #f59e0b; margin-top: 0;">⚠️ Requires Prior Authorization</h4>
            """, unsafe_allow_html=True)
            for service in coverage.get('requires_prior_auth', []):
                st.markdown(f'<div class="coverage-item">• {service}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with detail_col2:
        # Not covered
        if coverage.get('not_covered'):
            st.markdown("""
            <div class="coverage-section" style="border-left-color: #ef4444;">
            <h4 style="color: #ef4444; margin-top: 0;">❌ Not Covered</h4>
            """, unsafe_allow_html=True)
            for service in coverage.get('not_covered', []):
                st.markdown(f'<div class="coverage-item">• {service}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # In-network vs out-of-network
        if coverage.get('in_network_vs_out'):
            st.markdown("""
            <div class="coverage-section">
            <h4 style="color: #4da6ff; margin-top: 0;">🏥 Network Coverage</h4>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="coverage-item"><strong>In-Network:</strong><br>{coverage['in_network_vs_out'].get('in_network', 'N/A')}</div>
            <div class="coverage-item"><strong>Out-of-Network:</strong><br>{coverage['in_network_vs_out'].get('out_of_network', 'N/A')}</div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # Pharmacy benefits
    if coverage.get('pharmacy_benefits'):
        st.markdown(f"""
        <div class="coverage-section">
        <h4 style="color: #10b981; margin-top: 0;">💊 Pharmacy Benefits</h4>
        <div class="coverage-item">{coverage.get('pharmacy_benefits', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)

    # Interactive Q&A
    st.markdown("---")
    st.markdown("### 💬 Ask Questions About Your Coverage")

    user_question = st.text_input(
        "Ask anything about your insurance:",
        placeholder="e.g., Am I covered for physical therapy? What's my cost for an MRI?",
        key="coverage_question"
    )

    if user_question:
        with st.spinner("🤖 Thinking..."):
            from utils.claude_parser import answer_coverage_question
            answer = answer_coverage_question(coverage, user_question)
            st.markdown(f"""
            <div class="dark-card">
            <strong>Answer:</strong><br><br>
            {answer}
            </div>
            """, unsafe_allow_html=True)

    # Clear button
    st.markdown("---")
    if st.button("🗑️ Clear Insurance Data", type="secondary"):
        st.session_state.parsed_coverage = None
        st.session_state.insurance_data = None
        st.rerun()

def extract_insurance_params(coverage):
    """Extract numeric insurance parameters for cost calculator"""
    import re

    def extract_number(text):
        """Extract first number from text like '$2,000' or '20%'"""
        if not text or text == 'N/A':
            return 0
        match = re.search(r'[\d,]+', str(text).replace(',', ''))
        return int(match.group()) if match else 0

    def extract_percentage(text):
        """Extract percentage as decimal"""
        if not text or text == 'N/A':
            return 0.20  # default 20%
        match = re.search(r'(\d+)%', str(text))
        return int(match.group(1)) / 100 if match else 0.20

    return {
        "deductible_total": coverage.get('deductible_value', extract_number(coverage.get('deductible', '0'))),
        "deductible_met": 0,  # User will input this
        "coinsurance": coverage.get('coinsurance_value', extract_percentage(coverage.get('coinsurance', '20%'))),
        "oop_max": coverage.get('oop_max_value', extract_number(coverage.get('oop_max', '0'))),
        "oop_met": 0,  # User will input this
        "network": "in_network"
    }

def show_cost_estimator():
    """Display Enhanced Cost Estimator with multi-procedure selection"""

    st.title("💰 Personalized Cost Estimator")
    st.markdown("Select multiple procedures and see estimated costs from Dallas-area providers.")

    # Check if insurance data is loaded
    if st.session_state.insurance_data:
        st.success(f"✅ Using insurance from: {st.session_state.parsed_coverage.get('plan_name', 'Loaded Plan')}")
        
        # Get insurance params from session
        ins_data = st.session_state.insurance_data
        deductible_total = ins_data.get('deductible_total', 2000)
        coinsurance = ins_data.get('coinsurance', 0.20)
        oop_max = ins_data.get('oop_max', 6500)
        
        # Let user update their progress
        st.markdown("### 📊 Update Your Year-to-Date Spending")
        prog_col1, prog_col2 = st.columns(2)
        
        with prog_col1:
            deductible_met = st.number_input(
                f"Amount Paid Toward Deductible (${deductible_total:,} total)",
                min_value=0,
                max_value=deductible_total,
                value=ins_data.get('deductible_met', 0),
                step=100,
                key="deductible_progress"
            )
        
        with prog_col2:
            oop_met = st.number_input(
                f"Total Out-of-Pocket Paid (${oop_max:,} max)",
                min_value=0,
                max_value=oop_max,
                value=ins_data.get('oop_met', 0),
                step=100,
                key="oop_progress"
            )
    else:
        st.info("ℹ️ No insurance loaded. Enter your insurance details or try Demo Mode for sample data.")
        
        # Manual insurance entry
        st.markdown("### 🔧 Enter Your Insurance Information")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            deductible_total = st.number_input("Annual Deductible ($)", min_value=0, max_value=20000, value=2000, step=100)
            deductible_met = st.number_input("Amount Already Paid ($)", min_value=0, max_value=deductible_total, value=0, step=100)
        
        with col2:
            coinsurance_pct = st.number_input("Coinsurance (%)", min_value=0, max_value=100, value=20, step=5)
            coinsurance = coinsurance_pct / 100
        
        with col3:
            oop_max = st.number_input("Out-of-Pocket Maximum ($)", min_value=0, max_value=50000, value=6500, step=100)
            oop_met = st.number_input("OOP Already Paid ($)", min_value=0, max_value=oop_max, value=0, step=100)

    # Progress visualization
    st.markdown("### 📈 Your Coverage Progress")
    vis_col1, vis_col2 = st.columns(2)
    
    with vis_col1:
        ded_pct = min((deductible_met / deductible_total * 100) if deductible_total > 0 else 0, 100)
        st.progress(ded_pct / 100)
        st.caption(f"Deductible: ${deductible_met:,} / ${deductible_total:,} ({ded_pct:.0f}%)")
    
    with vis_col2:
        oop_pct = min((oop_met / oop_max * 100) if oop_max > 0 else 0, 100)
        st.progress(oop_pct / 100)
        st.caption(f"Out-of-Pocket Max: ${oop_met:,} / ${oop_max:,} ({oop_pct:.0f}%)")

    st.markdown("---")

    # Procedure selection by category
    st.markdown("### 🏥 Select Procedures")
    
    from utils.data_loader import get_procedure_categories
    categories = get_procedure_categories()
    
    selected_procedures = []
    
    for category, procedures in categories.items():
        with st.expander(f"**{category}**", expanded=True):
            for procedure in procedures:
                if st.checkbox(procedure, key=f"proc_{procedure}"):
                    selected_procedures.append(procedure)

    if not selected_procedures:
        st.info("👆 Select one or more procedures above to see cost estimates")
        return

    # Get estimates button
    if st.button("📊 Calculate Costs", type="primary", use_container_width=True):
        with st.spinner("🔍 Analyzing costs from Dallas providers..."):
            from utils.data_loader import get_dallas_providers_for_procedures
            from utils.cost_calculator import calculate_patient_responsibility
            
            # Get provider data
            providers = get_dallas_providers_for_procedures(selected_procedures)
            
            if not providers:
                st.error("No provider data available")
                return
            
            # Calculate costs for each provider
            all_estimates = []
            
            for provider in providers:
                provider_total_cost = 0
                provider_total_patient = 0
                running_deductible_met = deductible_met
                running_oop_met = oop_met
                procedure_details = []
                
                for proc_name in selected_procedures:
                    if proc_name in provider["procedures"]:
                        billed_amount = provider["procedures"][proc_name]
                        
                        # Calculate patient cost with running totals
                        insurance_params = {
                            "deductible_total": deductible_total,
                            "deductible_met": running_deductible_met,
                            "coinsurance": coinsurance,
                            "oop_max": oop_max,
                            "oop_met": running_oop_met
                        }
                        
                        patient_cost = calculate_patient_responsibility(billed_amount, insurance_params)
                        
                        # Update running totals
                        running_deductible_met = min(running_deductible_met + patient_cost, deductible_total)
                        running_oop_met = min(running_oop_met + patient_cost, oop_max)
                        
                        provider_total_cost += billed_amount
                        provider_total_patient += patient_cost
                        
                        procedure_details.append({
                            "procedure": proc_name,
                            "billed": billed_amount,
                            "patient_pays": patient_cost,
                            "insurance_pays": billed_amount - patient_cost
                        })
                
                all_estimates.append({
                    "provider": provider["provider_name"],
                    "type": provider["type"],
                    "address": provider["address"],
                    "distance": provider["distance"],
                    "quality": provider["quality_rating"],
                    "total_billed": provider_total_cost,
                    "total_patient": provider_total_patient,
                    "total_insurance": provider_total_cost - provider_total_patient,
                    "procedures": procedure_details
                })
            
            # Sort by patient cost
            all_estimates.sort(key=lambda x: x["total_patient"])
            
            # Display results
            st.markdown("### 💵 Cost Comparison Results")
            st.markdown(f"**Selected Procedures:** {', '.join(selected_procedures)}")
            
            # Summary metrics
            sum_col1, sum_col2, sum_col3 = st.columns(3)
            
            with sum_col1:
                avg_billed = sum(e["total_billed"] for e in all_estimates) / len(all_estimates)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Avg Billed Amount</div>
                    <div class="metric-value">${avg_billed:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with sum_col2:
                lowest_patient = all_estimates[0]["total_patient"]
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Lowest Your Cost</div>
                    <div class="metric-value" style="color: #10b981;">${lowest_patient:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with sum_col3:
                highest_patient = all_estimates[-1]["total_patient"]
                savings = highest_patient - lowest_patient
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Potential Savings</div>
                    <div class="metric-value" style="color: #f59e0b;">${savings:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Provider comparison
            st.markdown("### 🏥 Provider Comparison")
            
            for idx, estimate in enumerate(all_estimates):
                with st.expander(f"**#{idx+1} - {estimate['provider']}** - Your Cost: ${estimate['total_patient']:,.0f}", expanded=(idx==0)):
                    st.markdown(f"""
                    <div class="dark-card">
                    <strong>{estimate['type']}</strong><br>
                    📍 {estimate['address']}<br>
                    📏 {estimate['distance']} miles away<br>
                    {estimate['quality']} Quality Rating
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Cost breakdown
                    cost_col1, cost_col2, cost_col3 = st.columns(3)
                    
                    with cost_col1:
                        st.metric("Total Billed", f"${estimate['total_billed']:,.0f}")
                    with cost_col2:
                        st.metric("You Pay", f"${estimate['total_patient']:,.0f}", delta=f"-${estimate['total_billed'] - estimate['total_patient']:,.0f}" if estimate['total_patient'] < estimate['total_billed'] else None)
                    with cost_col3:
                        st.metric("Insurance Pays", f"${estimate['total_insurance']:,.0f}")
                    
                    # Procedure-by-procedure breakdown
                    st.markdown("**Procedure Breakdown:**")
                    import pandas as pd
                    proc_df = pd.DataFrame(estimate['procedures'])
                    proc_df['billed'] = proc_df['billed'].apply(lambda x: f"${x:,.0f}")
                    proc_df['patient_pays'] = proc_df['patient_pays'].apply(lambda x: f"${x:,.0f}")
                    proc_df['insurance_pays'] = proc_df['insurance_pays'].apply(lambda x: f"${x:,.0f}")
                    proc_df.columns = ['Procedure', 'Billed Amount', 'You Pay', 'Insurance Pays']
                    st.dataframe(proc_df, use_container_width=True, hide_index=True)
            
            # Visual comparison chart
            st.markdown("### 📊 Visual Cost Comparison")
            import plotly.graph_objects as go
            
            fig = go.Figure(data=[
                go.Bar(
                    name='You Pay',
                    x=[e['provider'] for e in all_estimates],
                    y=[e['total_patient'] for e in all_estimates],
                    marker_color='#4da6ff'
                ),
                go.Bar(
                    name='Insurance Pays',
                    x=[e['provider'] for e in all_estimates],
                    y=[e['total_insurance'] for e in all_estimates],
                    marker_color='#10b981'
                )
            ])
            
            fig.update_layout(
                barmode='stack',
                title='Cost Breakdown by Provider',
                xaxis_title='Provider',
                yaxis_title='Amount ($)',
                plot_bgcolor='#1e2530',
                paper_bgcolor='#1e2530',
                font=dict(color='#e0e0e0'),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Insurance math explanation
            with st.expander("🧮 How We Calculated Your Costs"):
                st.markdown(f"""
                <div class="info-card">
                <h4>Insurance Payment Waterfall:</h4>
                <ol>
                    <li><strong>Deductible First:</strong> You pay the first ${deductible_total:,} (you've paid ${deductible_met:,} so far)</li>
                    <li><strong>Then Coinsurance:</strong> After deductible, you pay {coinsurance*100:.0f}% of remaining costs</li>
                    <li><strong>Up to OOP Max:</strong> Once you've paid ${oop_max:,} total, insurance covers 100%</li>
                </ol>
                
                <p><strong>Note:</strong> Costs are calculated cumulatively across all selected procedures in the order they're performed.</p>
                </div>
                """, unsafe_allow_html=True)



if __name__ == "__main__":
    main()

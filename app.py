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

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    """Main application entry point"""

    # Sidebar navigation
    st.sidebar.title("🏥 Healthcare Transparency")
    st.sidebar.markdown("---")

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

    # Route to selected feature
    if feature == "🏠 Home":
        show_home()
    elif feature == "📋 Insurance Benefits Decoder":
        show_insurance_decoder()
    elif feature == "💰 Cost Estimator":
        show_cost_estimator()

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
    """Display Insurance Benefits Decoder feature"""

    st.title("📋 Insurance Benefits Decoder")
    st.markdown("Upload your insurance card or policy document to understand your coverage in plain English.")

    # Check API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        st.error("❌ **API Key Required**: Please set your Anthropic API key in the `.env` file.")
        st.code("ANTHROPIC_API_KEY=your_actual_api_key", language="bash")
        return

    # File upload section
    st.markdown("### Upload Your Insurance Document")

    col1, col2 = st.columns([2, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "Choose a file (PDF or Image)",
            type=["pdf", "png", "jpg", "jpeg"],
            help="Upload your insurance card (front and back) or policy document"
        )

    with col2:
        st.info(
            "**Accepted formats:**\n"
            "- PDF documents\n"
            "- Images (PNG, JPG)\n\n"
            "**What to upload:**\n"
            "- Insurance card\n"
            "- Policy documents\n"
            "- Benefits summary"
        )

    if uploaded_file is not None:
        # Display uploaded file info
        st.success(f"✅ Uploaded: {uploaded_file.name}")

        # Parse button
        if st.button("🔍 Analyze Document", type="primary"):
            with st.spinner("Analyzing your insurance document with AI..."):
                # Import the parser
                from utils.claude_parser import parse_insurance_document

                # Parse the document
                result = parse_insurance_document(uploaded_file)

                if result.get("success"):
                    # Display extracted information
                    st.markdown("### 📊 Your Coverage Summary")

                    # Key details in metrics
                    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)

                    with metrics_col1:
                        st.metric("Plan Name", result.get("plan_name", "N/A"))
                        st.metric("Annual Deductible", result.get("deductible", "N/A"))

                    with metrics_col2:
                        st.metric("Out-of-Pocket Max", result.get("oop_max", "N/A"))
                        st.metric("Primary Care Copay", result.get("copay_primary", "N/A"))

                    with metrics_col3:
                        st.metric("Specialist Copay", result.get("copay_specialist", "N/A"))
                        st.metric("Coinsurance", result.get("coinsurance", "N/A"))

                    # Detailed breakdown
                    with st.expander("📋 Detailed Coverage Breakdown", expanded=True):
                        st.markdown(result.get("plain_english_summary", ""))

                    # Network information
                    if result.get("network_info"):
                        with st.expander("🏥 Network Coverage"):
                            st.markdown(result.get("network_info", ""))

                    # Pharmacy benefits
                    if result.get("pharmacy_benefits"):
                        with st.expander("💊 Pharmacy Benefits"):
                            st.markdown(result.get("pharmacy_benefits", ""))

                    # Visual progress bars
                    st.markdown("### 📈 Coverage Progress (Example)")
                    deductible_progress = st.slider(
                        "How much have you paid toward your deductible this year?",
                        min_value=0,
                        max_value=10000,
                        value=0,
                        step=100,
                        help="Track your deductible progress"
                    )

                    # Chat interface
                    st.markdown("---")
                    st.markdown("### 💬 Ask Questions About Your Coverage")

                    user_question = st.text_input(
                        "Ask anything about your insurance:",
                        placeholder="e.g., Am I covered for physical therapy?"
                    )

                    if user_question:
                        with st.spinner("Thinking..."):
                            from utils.claude_parser import answer_coverage_question
                            answer = answer_coverage_question(result, user_question)
                            st.markdown(f"**Answer:** {answer}")

                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error occurred')}")

    else:
        # Show example/instructions
        st.markdown("### 👆 Upload a document to get started")
        st.markdown("""
        **What we'll extract:**
        - Plan name and type
        - Deductible amounts
        - Copay amounts (primary care, specialist, ER, urgent care)
        - Coinsurance percentages
        - Out-of-pocket maximum
        - In-network vs out-of-network coverage
        - Pharmacy benefits
        - And more...
        """)

def show_cost_estimator():
    """Display Personalized Cost Estimator feature"""

    st.title("💰 Personalized Cost Estimator")
    st.markdown("Estimate your actual out-of-pocket costs for common medical procedures.")

    # Insurance information input
    st.markdown("### 🔧 Your Insurance Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        deductible_total = st.number_input(
            "Annual Deductible ($)",
            min_value=0,
            max_value=20000,
            value=1500,
            step=100,
            help="Your total annual deductible"
        )

        deductible_met = st.number_input(
            "Amount Already Paid ($)",
            min_value=0,
            max_value=deductible_total,
            value=0,
            step=100,
            help="How much you've paid toward your deductible this year"
        )

    with col2:
        coinsurance = st.number_input(
            "Coinsurance (%)",
            min_value=0,
            max_value=100,
            value=20,
            step=5,
            help="Your coinsurance percentage (you pay this % after deductible)"
        )

        oop_max = st.number_input(
            "Out-of-Pocket Maximum ($)",
            min_value=0,
            max_value=50000,
            value=6000,
            step=100,
            help="Maximum you'll pay in a year"
        )

    with col3:
        oop_met = st.number_input(
            "OOP Already Paid ($)",
            min_value=0,
            max_value=oop_max,
            value=0,
            step=100,
            help="How much you've paid toward your OOP max"
        )

    # Progress bars
    st.markdown("#### Your Progress This Year")
    progress_col1, progress_col2 = st.columns(2)

    with progress_col1:
        deductible_pct = min((deductible_met / deductible_total * 100) if deductible_total > 0 else 0, 100)
        st.progress(deductible_pct / 100)
        st.caption(f"Deductible: ${deductible_met:,.0f} / ${deductible_total:,.0f} ({deductible_pct:.0f}%)")

    with progress_col2:
        oop_pct = min((oop_met / oop_max * 100) if oop_max > 0 else 0, 100)
        st.progress(oop_pct / 100)
        st.caption(f"Out-of-Pocket Max: ${oop_met:,.0f} / ${oop_max:,.0f} ({oop_pct:.0f}%)")

    st.markdown("---")

    # Procedure selection
    st.markdown("### 🏥 Select a Procedure")

    procedure = st.selectbox(
        "Choose a medical procedure:",
        [
            "MRI - Brain (with contrast)",
            "MRI - Knee",
            "CT Scan - Chest",
            "CT Scan - Abdomen",
            "Emergency Room Visit - Level 3",
            "Emergency Room Visit - Level 4",
            "Urgent Care Visit",
            "Specialist Office Visit",
            "Primary Care Office Visit",
            "Colonoscopy (screening)",
            "X-Ray - Chest",
            "Ultrasound - Abdomen"
        ]
    )

    # Location filter
    location_col1, location_col2 = st.columns(2)

    with location_col1:
        zip_code = st.text_input(
            "ZIP Code",
            placeholder="Enter ZIP code",
            max_chars=5,
            help="Find providers near you"
        )

    with location_col2:
        radius = st.slider(
            "Search Radius (miles)",
            min_value=5,
            max_value=50,
            value=10,
            step=5
        )

    # Estimate button
    if st.button("📊 Get Cost Estimates", type="primary"):
        with st.spinner("Fetching real pricing data from CMS..."):
            from utils.cost_calculator import calculate_cost_estimates
            from utils.data_loader import load_cms_data

            # Load CMS data
            cms_data = load_cms_data(procedure, zip_code, radius)

            # Calculate estimates
            insurance_params = {
                "deductible_total": deductible_total,
                "deductible_met": deductible_met,
                "coinsurance": coinsurance / 100,
                "oop_max": oop_max,
                "oop_met": oop_met
            }

            estimates = calculate_cost_estimates(cms_data, insurance_params)

            if estimates:
                # Display results
                st.markdown("### 💵 Cost Comparison Results")

                # Summary stats
                stats_col1, stats_col2, stats_col3 = st.columns(3)

                with stats_col1:
                    avg_price = sum(e["billed_amount"] for e in estimates) / len(estimates)
                    st.metric("Average Billed Amount", f"${avg_price:,.0f}")

                with stats_col2:
                    avg_oop = sum(e["your_cost"] for e in estimates) / len(estimates)
                    st.metric("Avg Your Cost", f"${avg_oop:,.0f}")

                with stats_col3:
                    price_range = max(e["billed_amount"] for e in estimates) - min(e["billed_amount"] for e in estimates)
                    st.metric("Price Range", f"${price_range:,.0f}")

                # Provider comparison table
                st.markdown("#### 🏥 Provider Comparison")

                import pandas as pd
                import plotly.express as px

                df = pd.DataFrame(estimates)

                # Sort by your cost
                df = df.sort_values("your_cost")

                # Display table
                st.dataframe(
                    df[[
                        "provider_name",
                        "distance_miles",
                        "billed_amount",
                        "your_cost",
                        "surprise_bill_risk"
                    ]],
                    use_container_width=True,
                    hide_index=True
                )

                # Bar chart comparison
                st.markdown("#### 📊 Visual Comparison")

                fig = px.bar(
                    df,
                    x="provider_name",
                    y=["billed_amount", "your_cost"],
                    barmode="group",
                    title="Billed Amount vs Your Estimated Cost",
                    labels={
                        "value": "Amount ($)",
                        "provider_name": "Provider",
                        "variable": "Cost Type"
                    }
                )

                st.plotly_chart(fig, use_container_width=True)

                # Map view placeholder
                st.markdown("#### 🗺️ Map View")
                st.info("🗺️ Interactive map view coming soon! Will show provider locations with cost indicators.")

                # Surprise bill warnings
                high_risk_providers = [e for e in estimates if e["surprise_bill_risk"] == "High"]
                if high_risk_providers:
                    st.warning(
                        f"⚠️ **Surprise Bill Risk Alert**: {len(high_risk_providers)} provider(s) have high surprise billing risk. "
                        "These facilities may have out-of-network specialists or services."
                    )

                # Cost breakdown for selected provider
                with st.expander("🧮 Detailed Cost Calculation (First Provider)"):
                    selected = estimates[0]
                    st.markdown(f"""
                    **Provider:** {selected['provider_name']}

                    **How we calculated your cost:**
                    1. **Billed Amount:** ${selected['billed_amount']:,.0f}
                    2. **Remaining Deductible:** ${deductible_total - deductible_met:,.0f}
                    3. **Amount Applied to Deductible:** ${min(selected['billed_amount'], deductible_total - deductible_met):,.0f}
                    4. **Amount Subject to Coinsurance:** ${max(0, selected['billed_amount'] - (deductible_total - deductible_met)):,.0f}
                    5. **Your Coinsurance ({coinsurance}%):** ${max(0, selected['billed_amount'] - (deductible_total - deductible_met)) * (coinsurance/100):,.0f}
                    6. **Your Total Cost:** ${selected['your_cost']:,.0f}

                    *(This assumes in-network pricing and that you haven't reached your out-of-pocket maximum)*
                    """)

            else:
                st.warning("No pricing data available for this procedure in your area. Try a different ZIP code or procedure.")

if __name__ == "__main__":
    main()

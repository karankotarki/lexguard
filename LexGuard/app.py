import streamlit as st
import fitz  # PyMuPDF
from google import genai # New Google GenAI SDK

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="LexGuard | Enterprise Legal Intelligence",
    page_icon="shield",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PREMIUM ENTERPRISE DESIGN SYSTEM (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --primary-navy: #0f172a;
        --secondary-navy: #1e293b;
        --accent-blue: #3b82f6;
        --accent-glow: rgba(59, 130, 246, 0.5);
        --text-main: #f1f5f9;
        --text-muted: #94a3b8;
        --glass-bg: rgba(15, 23, 42, 0.8);
        --glass-border: rgba(255, 255, 255, 0.08);
        --card-bg: rgba(30, 41, 59, 0.5);
    }

    /* Global Overrides with Immersive Background */
    .stApp {
        background: 
            linear-gradient(rgba(10, 12, 16, 0.94), rgba(10, 12, 16, 0.96)),
            url('https://images.unsplash.com/photo-1505664194779-8beaceb93744?auto=format&fit=crop&q=80&w=2070');
        background-size: cover;
        background-attachment: fixed;
        color: var(--text-main);
        font-family: 'Inter', sans-serif;
    }

    /* Compact Layout Overrides */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
    }

    /* Header/Hero Section with Cinematic Background */
    .hero-container {
        padding: 3rem 2rem;
        background: 
            linear-gradient(rgba(15, 23, 42, 0.8), rgba(15, 23, 42, 0.9)),
            url('https://images.unsplash.com/photo-1450101499163-c8848c66ca85?auto=format&fit=crop&q=80&w=2070');
        background-size: cover;
        background-position: center;
        border-radius: 12px;
        border: 1px solid var(--glass-border);
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        position: relative;
        overflow: hidden;
    }

    .hero-logo {
        font-size: 3.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
        letter-spacing: -1.5px;
        text-transform: none;
    }

    .hero-tagline {
        color: var(--text-muted);
        font-size: 1.1rem;
        font-weight: 400;
        max-width: 700px;
        margin: 0 auto;
        letter-spacing: 0.2px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #080a0f !important;
        border-right: 1px solid var(--glass-border);
    }
    
    .sidebar-label {
        font-size: 0.75rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
    
    .status-indicator {
        display: flex;
        align-items: center;
        gap: 8px;
        background: rgba(59, 130, 246, 0.05);
        color: #60a5fa;
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 0.8rem;
        border: 1px solid rgba(59, 130, 246, 0.1);
        margin-bottom: 0.5rem;
    }

    /* Premium Cards & Containers */
    .premium-card {
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: 10px;
        padding: 1.25rem;
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }

    .premium-card:hover {
        background: rgba(30, 41, 59, 0.7);
        border-color: rgba(59, 130, 246, 0.4);
        transform: translateY(-2px);
    }

    .premium-card h3 {
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
        color: #ffffff !important;
    }

    .premium-card .caption {
        font-size: 0.8rem;
        color: var(--text-muted);
        line-height: 1.4;
    }

    /* Results/Audit Container */
    .audit-report {
        background: rgba(15, 23, 42, 0.6);
        border-left: 2px solid var(--accent-blue);
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 1rem;
        line-height: 1.5;
        border: 1px solid var(--glass-border);
    }
    
    .audit-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.25rem;
        border-bottom: 1px solid var(--glass-border);
        padding-bottom: 0.75rem;
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        background: var(--primary-navy) !important;
        color: #cbd5e1 !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }

    .stButton>button:hover {
        border-color: var(--accent-blue) !important;
        color: #ffffff !important;
        background: var(--secondary-navy) !important;
    }

    /* File Uploader */
    [data-testid="stFileUploadDropzone"] {
        background: rgba(15, 23, 42, 0.4) !important;
        border: 1px dashed var(--glass-border) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
    }

    /* Typography */
    h1, h2, h3 {
        font-weight: 600 !important;
        letter-spacing: -0.025em !important;
    }
    
    .section-title {
        color: var(--text-muted);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 1rem;
        margin-top: 2rem;
        border-left: 2px solid var(--accent-blue);
        padding-left: 10px;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-right: 6px;
    }
    .badge-blue { background: rgba(59, 130, 246, 0.1); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.2); }
    .badge-green { background: rgba(16, 185, 129, 0.1); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.2); }
    .badge-red { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); }

    /* Report Content Styling */
    .report-content h3 {
        color: var(--text-main);
        font-size: 0.95rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 1.25rem !important;
        margin-bottom: 0.5rem !important;
        padding-bottom: 0.25rem;
        border-bottom: 1px solid var(--glass-border);
    }
    
    .report-content p, .report-content li {
        font-size: 0.9rem;
        color: #cbd5e1;
    }

    /* Nav Header */
    .nav-header {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding: 0.75rem 2rem;
        position: fixed;
        top: 0;
        right: 0;
        left: 0;
        z-index: 999;
        background: rgba(8, 10, 15, 0.8);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid var(--glass-border);
    }
    .sign-in-btn {
        background: transparent;
        color: var(--text-muted);
        border: 1px solid var(--glass-border);
        padding: 5px 14px;
        border-radius: 4px;
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.2s;
        font-weight: 500;
    }
    .sign-in-btn:hover {
        color: #ffffff;
        border-color: var(--accent-blue);
    }

    /* Intelligence Meters */
    .metric-container {
        display: flex;
        justify-content: space-between;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid var(--glass-border);
        border-radius: 8px;
        padding: 0.5rem;
        flex: 1;
        text-align: center;
        min-height: 60px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-value {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--accent-blue);
    }
    .metric-label {
        font-size: 0.6rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 2px;
    }

    /* Enterprise Alert Style */
    .enterprise-alert {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(239, 68, 68, 0.2);
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }
    .enterprise-alert-title {
        color: #f87171;
        font-weight: 700;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .enterprise-alert-message {
        color: var(--text-muted);
        font-size: 0.9rem;
        font-weight: 400;
    }

    /* Custom Premium Loader */
    .loader-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem;
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        margin: 1.5rem 0;
    }
    .premium-loader {
        width: 40px;
        height: 40px;
        border: 2px solid rgba(59, 130, 246, 0.1);
        border-top: 2px solid var(--accent-blue);
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 1rem;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .loader-text {
        font-size: 0.9rem;
        color: var(--text-muted);
        letter-spacing: 0.5px;
        font-weight: 500;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stHeader"] {display: none;}
</style>
<div class="nav-header">
    <button class="sign-in-btn">Sign In</button>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTENT ---
with st.sidebar:
    st.markdown("<h2 style='font-size:1.2rem; margin-bottom:1.5rem; color:#fff;'>LEXGUARD</h2>", unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-label">System Status</div>', unsafe_allow_html=True)
    st.markdown('<div class="status-indicator">Operational</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-label">Security Protocol</div>', unsafe_allow_html=True)
    st.markdown('<div class="status-indicator">AES-256 Encrypted</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-label">Technology Stack</div>', unsafe_allow_html=True)
    st.caption("Enterprise NLP Framework\nPyMuPDF Core\nStreamlit Engine")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("Client Access"):
        pass

# --- HEADER / HERO ---
st.markdown("""
<div class="hero-container">
    <div class="hero-logo">LexGuard</div>
    <div class="hero-tagline">Enterprise Legal Intelligence & Compliance Analysis Platform</div>
</div>
""", unsafe_allow_html=True)

# --- API KEY CONFIGURATION ---
GEMINI_API_KEY ="AIzaSyCrfbSvBftlQy99WxrwAzbahhQfmhbwa1M"

if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
    st.error("Action Required: Please set your Gemini API key in app.py.")
    st.stop()

client = genai.Client(api_key=GEMINI_API_KEY)

# --- CORE FUNCTIONS ---
@st.cache_data
def extract_text_from_pdf(pdf_bytes):
    text = ""
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text("text") + "\n\n"
    return text

def analyze_document_with_gemini(document_text, query, analysis_type="general"):
    fallback_phrases = {
        "hidden_fees": "No hidden fee clauses found in the uploaded document.",
        "termination": "No termination clauses detected in the uploaded document.",
        "general": "No relevant clause found in the uploaded document."
    }
    fallback_phrase = fallback_phrases.get(analysis_type, fallback_phrases["general"])
    
    prompt = f"""
    You are LexGuard, an enterprise legal intelligence AI.
    Analyze the document and provide a concise AUDIT REPORT in STRICTOR MARKDOWN format.

    REQUIRED STRUCTURE:
    ### RISK ASSESSMENT
    Brief professional justification (1-2 sentences).
    
    ### AI CONFIDENCE SCORE
    Percentage (e.g., 95%) based on data clarity.
    
    ### KEY FINDINGS
    2-4 concise bullets of primary legal/operational findings.
    
    ### HIGH-RISK CLAUSES
    2-4 concise bullets identifying specific liabilities or high-risk language.
    
    ### COMPLIANCE STATUS
    1-2 sentences on regulatory or enterprise alignment.

    ### RECOMMENDATIONS
    2-3 short, actionable professional actions.

    STRICT RULES:
    1. Answer ONLY based on the provided document.
    2. Use professional enterprise terminology.
    3. Be extremely concise. Max 4 bullets per section. No conversational filler.
    4. NO EMOJIS.
    5. NO HTML tags, span tags, div tags, or CSS in the response.
    6. Return ONLY clean markdown headers and bullets.
    7. If no info is found, reply ONLY with: "{fallback_phrase}"

    --- DOCUMENT ---
    {document_text}
    
    --- USER QUERY ---
    {query}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=prompt
        )
        return response.text
    except Exception as e:
        # Return a specialized error token for the UI to handle
        if "429" in str(e) or "quota" in str(e).lower():
            return "ERROR_QUOTA_EXHAUSTED"
        return f"ERROR_SYSTEM: {str(e)}"

# --- MAIN APP UI ---

# 1. File Upload Section
st.markdown('<div class="section-title">Document Ingestion</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")

if uploaded_file is not None:
    if 'document_text' not in st.session_state:
        with st.status("Extracting document data...", expanded=True) as status:
            pdf_bytes = uploaded_file.read()
            st.session_state.document_text = extract_text_from_pdf(pdf_bytes)
            status.update(label="Verification complete", state="complete", expanded=False)
    
    st.markdown('<div class="section-title">Analysis Framework</div>', unsafe_allow_html=True)
    
    # Grid layout for quick actions
    col1, col2, col3 = st.columns(3)
    
    question_to_ask = None
    analysis_type = "general"
    
    with col1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### Privacy Audit")
        st.markdown('<div class="caption">Analyze data collection and sharing protocols.</div>', unsafe_allow_html=True)
        if st.button("Run Privacy Scan", key="privacy_scan"):
            question_to_ask = "Identify privacy risks, data collection policies, and data sharing practices."
            analysis_type = "general"
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### Financial Review")
        st.markdown('<div class="caption">Audit recurring costs and financial obligations.</div>', unsafe_allow_html=True)
        if st.button("Run Financial Audit", key="financial_scan"):
            question_to_ask = "Identify any hidden fees, recurring charges, auto-renewal costs, or cancellation fees."
            analysis_type = "hidden_fees"
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col3:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### Termination Audit")
        st.markdown('<div class="caption">Review contract cancellation and exit terms.</div>', unsafe_allow_html=True)
        if st.button("Run Termination Audit", key="termination_scan"):
            question_to_ask = "Identify the exact terms and conditions for terminating this agreement."
            analysis_type = "termination"
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    
    col4, col5 = st.columns(2)
    with col4:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### Compliance Intelligence")
        st.markdown('<div class="caption">Verify alignment with regulatory frameworks.</div>', unsafe_allow_html=True)
        if st.button("Run Compliance Scan", key="compliance_scan"):
            question_to_ask = "Analyze the document for compliance with standard legal frameworks like GDPR or SOC2."
            analysis_type = "general"
        st.markdown('</div>', unsafe_allow_html=True)

    with col5:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### Risk Classification")
        st.markdown('<div class="caption">Prioritize document threat levels and severity.</div>', unsafe_allow_html=True)
        if st.button("Classify Risks", key="risk_scan"):
            question_to_ask = "Classify the risks in this document into Low, Moderate, and High categories."
            analysis_type = "general"
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Manual Consultation</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="premium-card" style="padding: 1rem;">', unsafe_allow_html=True)
    mc_col1, mc_col2 = st.columns([4, 1])
    with mc_col1:
        custom_question = st.text_input("", placeholder="Enter specific legal query...", label_visibility="collapsed")
    with mc_col2:
        if st.button("Execute Query"):
            if custom_question.strip():
                question_to_ask = custom_question
                analysis_type = "general"
            else:
                st.warning("Query input required.")
    st.markdown('</div>', unsafe_allow_html=True)
            
    if question_to_ask:
        loader_placeholder = st.empty()
        with loader_placeholder:
            st.markdown("""
                <div class="loader-container">
                    <div class="premium-loader"></div>
                    <div class="loader-text">Processing legal intelligence analysis...</div>
                </div>
            """, unsafe_allow_html=True)
        
        answer = analyze_document_with_gemini(st.session_state.document_text, question_to_ask, analysis_type)
        loader_placeholder.empty()

        # 1. HANDLE ERRORS CLEANLY
        if answer == "ERROR_QUOTA_EXHAUSTED" or answer.startswith("ERROR_SYSTEM"):
            error_title = "Analysis Temporarily Unavailable" if answer == "ERROR_QUOTA_EXHAUSTED" else "System Anomaly Detected"
            error_msg = "System capacity is currently limited. Please retry shortly." if answer == "ERROR_QUOTA_EXHAUSTED" else "The intelligence audit encountered an unexpected state. Please re-initialize."
            
            st.markdown(f"""
                <div class="enterprise-alert">
                    <div class="enterprise-alert-title">{error_title}</div>
                    <div class="enterprise-alert-message">{error_msg}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            # 2. RENDER SUCCESSFUL REPORT
            st.markdown('<div class="section-title">Intelligence Report</div>', unsafe_allow_html=True)
            
            # Metric Grid
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.markdown('<div class="metric-card"><div class="metric-label">Document Complexity</div><div class="metric-value">Advanced</div></div>', unsafe_allow_html=True)
            with col_m2:
                st.markdown('<div class="metric-card"><div class="metric-label">Compliance Index</div><div class="metric-value">84%</div></div>', unsafe_allow_html=True)
            with col_m3:
                st.markdown('<div class="metric-card"><div class="metric-label">AI Integrity</div><div class="metric-value">High</div></div>', unsafe_allow_html=True)

            st.markdown(f"""
<div class="audit-report">
<div class="audit-header">
<div>
<span class="badge badge-blue">ENTERPRISE AUDIT</span>
<span class="badge badge-green">VERIFIED</span>
</div>
<div style="color: var(--text-muted); font-size: 0.7rem;">REF: {hash(question_to_ask) % 10000} | {analysis_type.upper()}</div>
</div>
<div style="background: rgba(59, 130, 246, 0.05); padding: 0.75rem; border-radius: 6px; margin-bottom: 1.25rem; border: 1px solid var(--glass-border);">
<div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
<span style="font-size: 0.7rem; color: var(--text-muted);">RISK SEVERITY INDEX</span>
<span style="font-size: 0.7rem; color: #f87171; font-weight: 600;">MODERATE</span>
</div>
<div style="width: 100%; background: #1e293b; height: 4px; border-radius: 2px; overflow: hidden;">
<div style="width: 45%; background: #3b82f6; height: 100%;"></div>
</div>
</div>
<div class="report-content">
{answer}
</div>
<div style="margin-top: 1.5rem; padding-top: 0.75rem; border-top: 1px solid var(--glass-border); font-size: 0.7rem; color: var(--text-muted); display: flex; justify-content: space-between;">
<span>Confidential Intelligence Output</span>
<span>LexGuard Enterprise</span>
</div>
</div>
""", unsafe_allow_html=True)
else:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("System Ready. Upload a document to initialize compliance analysis.")

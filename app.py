import streamlit as st
import os
import requests
import PyPDF2

# --- 1. CONFIG & BRANDING ---
st.set_page_config(page_title="Draft Auditor AI", layout="wide", page_icon="⚖️")

# --- 2. PROFESSIONAL CSS ---
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .price-card { padding: 15px; border-radius: 10px; background: white; border-top: 5px solid #007bff; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; }
    .report-section { background: white; padding: 20px; border-radius: 10px; border-left: 5px solid #28a745; margin-bottom: 10px; }
    .stButton>button { background-color: #007bff; color: white; font-weight: bold; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# --- 3. SECRETS ---
API_KEY = os.environ.get("OPENROUTER_API_KEY")
APP_PASS = os.environ.get("APP_PASSWORD")

if 'auth' not in st.session_state: st.session_state.auth = False

# --- 4. SECURE LOGIN ---
if not st.session_state.auth:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://img.icons8.com/fluency/96/checked-user-male.png", width=80)
        st.subheader("Draft Auditor: Restricted Access")
        pwd = st.text_input("Enter Founder/Investor Key", type="password")
        if st.button("Unlocking Global Dashboard"):
            if pwd == APP_PASS:
                st.session_state.auth = True
                st.rerun()
            else: st.error("❌ Unauthorized Access")
    st.stop()

# --- 5. MAIN DASHBOARD ---
st.title("⚖️ Draft Auditor: Enterprise AI")
st.write("Professional Legal Document Screening & Risk Assessment.")

# --- 6. PRICE LIST SECTION (Investor Delight) ---
st.markdown("### 💰 Audit Pricing Models")
p_col1, p_col2, p_col3 = st.columns(3)
with p_col1:
    st.markdown("<div class='price-card'><h4>Standard (India)</h4><h2>₹59</h2><p>Per Document Scan</p></div>", unsafe_allow_html=True)
with p_col2:
    st.markdown("<div class='price-card'><h4>Global (Dubai)</h4><h2>$0.99</h2><p>Per Document Scan</p></div>", unsafe_allow_html=True)
with p_col3:
    st.markdown("<div class='price-card'><h4>Enterprise</h4><h2>Custom</h2><p>API for Law Firms</p></div>", unsafe_allow_html=True)

st.write("---")

# --- 7. UPLOAD & ANALYSIS ---
uploaded_file = st.file_uploader("Upload Agreement (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file:
    if st.button("🚀 Start Deep AI Audit"):
        with st.spinner("AI Brain (Gemini 2.0) is reading the fine print..."):
            # Text extraction (PDF focus)
            content = ""
            if uploaded_file.type == "application/pdf":
                reader = PyPDF2.PdfReader(uploaded_file)
                for page in reader.pages: content += page.extract_text()
            else:
                content = "This is an image-based legal document. Please perform OCR and analyze."

            # AI CALL (OpenRouter)
            prompt = f"Analyze this legal draft and provide a professional report in 4 parts: 1. Risk Summary, 2. Financial Trap Check, 3. Missing Clauses, 4. Final Score (0-100). Text: {content[:4000]}"
            
            try:
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    json={
                        "model": "google/gemini-2.0-flash-001",
                        "messages": [{"role": "user", "content": prompt}]
                    }
                )
                report = response.json()['choices'][0]['message']['content']
                
                # Showing Results
                st.markdown("### 📊 AI Audit Report")
                st.markdown(f"<div class='report-section'>{report}</div>", unsafe_allow_html=True)
                st.download_button("📩 Download Audit Report", report, file_name="Draft_Audit_Report.txt")
                
            except Exception as e:
                st.error(f"API Connection Error! Check your OpenRouter Key. {e}")

# Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.write("📍 **Status:** Global Prototype")
st.sidebar.write("🏢 **Project:** Draft Auditor AI")
if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.rerun()

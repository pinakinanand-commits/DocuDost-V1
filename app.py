import streamlit as st
import google.generativeai as genai
import os

# --- ADVANCED CONFIGURATION ---
st.set_page_config(page_title="DocuDost AI | Legal Auditor", layout="wide")

# Custom CSS for Professional "Audit Boxes"
st.markdown("""
    <style>
    .risk-high { background-color: #ffcccc; padding: 10px; border-radius: 5px; border-left: 5px solid red; margin-bottom: 10px; }
    .risk-safe { background-color: #ccffcc; padding: 10px; border-radius: 5px; border-left: 5px solid green; margin-bottom: 10px; }
    .header-style { font-size: 25px; font-weight: bold; color: #1E3A8A; }
    </style>
    """, unsafe_allow_html=True)

# --- GOOGLE GEMINI SETUP ---
# Securely getting API Key (Hugging Face Secrets mein 'GOOGLE_API_KEY' naam se save karein)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Advanced System Instruction for Google Evaluation
SYSTEM_PROMPT = """
You are the DocuDost AI Legal Auditor. Your task is to perform a high-precision audit of legal contracts.
For every document:
1. Identify hidden risks, unfair clauses, and 'traps'.
2. Categorize them as 'HIGH RISK' (Red) or 'SAFE/STANDARD' (Green).
3. Provide a clear 'Simple English' explanation for common people.
4. Suggest a counter-clause to protect the user.
Format your response as a professional audit report.
"""

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction=SYSTEM_PROMPT
)

# --- UI LAYOUT ---
st.markdown('<p class="header-style">🛡️ DocuDost AI: Advanced Legal Auditor</p>', unsafe_allow_html=True)
st.info("Directly auditing via Google Gemini 2.0 Flash Engine | Secure & Stateless")

uploaded_file = st.file_file_uploader("Upload Contract (PDF or Image)", type=['pdf', 'jpg', 'png'])

if uploaded_file is not None:
    if st.button("🚀 Start Deep Audit"):
        with st.spinner("Analyzing clauses for hidden traps..."):
            try:
                # Processing (Simulated for this snippet - use your PDF-to-Text logic here)
                content = uploaded_file.read() # Basic read
                
                # AI Call
                response = model.generate_content(f"Audit this document: {content}")
                
                st.subheader("Audit Results")
                st.markdown(response.text)
                
                st.success("Audit Complete. No data was stored on our servers.")
                
            except Exception as e:
                st.error(f"Technical Error: {e}")

# --- FOOTER FOR GOOGLE ACCELERATOR ---
st.markdown("---")
st.caption("DocuDost AI Prototype | Built for Google for Startups Accelerator 2026")

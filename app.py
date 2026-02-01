import streamlit as st
import google.generativeai as genai
from PIL import Image

# Page Setup
st.set_page_config(page_title="DocuDost AI", page_icon="🛡️", layout="centered")
st.title("🛡️ DocuDost: Professional AI Auditor")
st.markdown("---")

# Sidebar for Key
with st.sidebar:
    st.header("Authentication")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Get your key: [Google AI Studio](https://aistudio.google.com/)")

# File Uploader
uploaded_file = st.file_uploader("Upload Legal Document (Image)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Document Preview", use_container_width=True)
    
    if st.button("🚀 Run Professional Audit"):
        if not api_key:
            st.error("Please enter your API Key in the sidebar!")
        else:
            try:
                genai.configure(api_key=api_key.strip())
                
                # We try 'gemini-1.5-flash' first, then 'gemini-pro-vision'
                model_name = 'gemini-1.5-flash'
                model = genai.GenerativeModel(model_name)
                
                with st.spinner(f'Analyzing using {model_name}...'):
                    prompt = "You are a senior lawyer. Analyze this document and list 3 major risks and a safety score (0-100) in professional Hinglish."
                    response = model.generate_content([prompt, img])
                    
                    st.success("Audit Completed Successfully!")
                    st.markdown("### 📋 Audit Report")
                    st.write(response.text)
                    
            except Exception as e:
                # This is the 'except' block that was missing!
                st.error(f"Technical Notice: {str(e)}")
                st.info("Try updating the model name in code if 404 persists.")

# Footer
st.markdown("---")
st.caption("DocuDost AI Prototype v1.0 | Confidential")

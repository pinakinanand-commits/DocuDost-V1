import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="DocuDost AI", page_icon="🛡️")
st.title("🛡️ DocuDost: AI Legal Auditor")

with st.sidebar:
    api_key = st.text_input("Enter Gemini API Key", type="password")

uploaded_file = st.file_uploader("Upload Document Image", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    st.image(img, caption="Document Loaded", width=300)
    
    if st.button("Analyze Document"):
        try:
            # Step 1: Configuration
            genai.configure(api_key=api_key.strip())
            
            # Step 2: Using the most stable model name for v1beta
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            with st.spinner('Scanning Document...'):
                response = model.generate_content([
                    "Analyze this document and list 3 legal risks in Hinglish.", 
                    img
                ])
                st.markdown("### 📋 Audit Report")
                st.write(response.text)
                
        except Exception as e:
            # Yeh block hona zaroori hai SyntaxError hatane ke liye
            st.error(f"Error: {e}")
            st.info("Check if your API Key is correct and active.")

elif not api_key and uploaded_file:
    st.warning("Please enter your API Key in the sidebar.")

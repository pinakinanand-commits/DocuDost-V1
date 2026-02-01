import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

st.set_page_config(page_title="DocuDost AI", page_icon="🛡️")
st.title("🛡️ DocuDost: AI Legal Auditor")

# API Key input
with st.sidebar:
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Get key: aistudio.google.com")

uploaded_file = st.file_uploader("Upload Document (Image)", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    st.image(img, caption="Document Loaded", width=300)
    
    if st.button("🚀 Analyze Now"):
        try:
            # Force setting the API key
            genai.configure(api_key=api_key.strip())
            
            # Use the most stable model name
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner('Analyzing with Google AI...'):
                # Content generation
                response = model.generate_content([
                    "Analyze this document image. Identify the document type and list 3 potential legal risks in Hinglish.", 
                    img
                ])
                
                if response.text:
                    st.success("Analysis Ready!")
                    st.markdown("### 📋 Professional Audit Report")
                    st.write(response.text)
                else:
                    st.error("AI couldn't read the image. Please try a clearer photo.")
                    
        except Exception as e:
            # Detailed Error for debugging
            st.error(f"Technical Error: {str(e)}")
            st.info("Tip: Check if your API Key is active at Google AI Studio.")

elif not api_key and uploaded_file:
    st.warning("Please enter your API Key in the sidebar.")

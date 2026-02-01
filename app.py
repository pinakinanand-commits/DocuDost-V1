import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="DocuDost AI", page_icon="🛡️")
st.title("🛡️ DocuDost: AI Legal Auditor")

with st.sidebar:
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Get your key from: aistudio.google.com")

uploaded_file = st.file_uploader("Upload Agreement (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    st.image(img, caption="Document Loaded", width=300)
    
    if st.button("Analyze Document"):
        try:
            # Step 1: Configure AI
            genai.configure(api_key=api_key.strip())
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Step 2: Show loading and get response
            with st.spinner('Scanning legal clauses...'):
                response = model.generate_content([
                    "You are a legal expert. Audit this document and list 3 critical risks in Hinglish.", 
                    img
                ])
                st.success("Analysis Done!")
                st.markdown("### 📋 Audit Report")
                st.write(response.text)
                
        except Exception as e:
            # Yeh woh 'except' block hai jiski wajah se error aa raha tha
            st.error(f"Something went wrong: {e}")

elif not api_key and uploaded_file:
    st.warning("Please enter your API Key in the sidebar to proceed.")

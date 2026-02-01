import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="DocuDost AI", page_icon="🛡️")
st.title("🛡️ DocuDost: AI Legal Auditor")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Tip: Create a NEW key at aistudio.google.com")

uploaded_file = st.file_uploader("Upload Document Image", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    st.image(img, caption="Document Loaded", use_column_width=True)
    
    if st.button("Analyze Document"):
        try:
            # Setting up the API
            genai.configure(api_key=api_key.strip())
            
            # Using the absolute stable model name
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner('DocuDost AI is reading your document...'):
                # Analyzing
                response = model.generate_content([
                    "You are a legal expert. Analyze this document and list 3 major risks in Hinglish. Be concise.", 
                    img
                ])
                
                st.success("Analysis Complete!")
                st.markdown("### 📋 Audit Report")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Technical Error: {e}")
            st.warning("Bhai, agar 404 aaye toh Streamlit Dashboard se 'Reboot App' zaroor karein.")

elif not api_key and uploaded_file:
    st.warning("Please enter your API Key in the sidebar.")

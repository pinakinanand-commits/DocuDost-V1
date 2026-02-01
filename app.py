import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="DocuDost AI", page_icon="🛡️")
st.title("🛡️ DocuDost: AI Legal Auditor")

# Sidebar for API Key
with st.sidebar:
    api_key = st.text_input("Enter Gemini API Key", type="password")

uploaded_file = st.file_uploader("Upload Agreement (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    st.image(img, caption="Document Loaded", width=300)
    
    if st.button("Analyze Document"):
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
if st.button("Analyze Document"):
    try:
        genai.configure(api_key=api_key.strip()) # strip() space hata dega
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Image ko sahi format mein bhejna
        response = model.generate_content([
            "Audit this legal document image and list 3 risks in Hinglish.", 
            img
        ])
        
        st.markdown("### 📋 Audit Report")
        st.write(response.text)
    except Exception as e:
        st.error(f"AI Error: {e}")

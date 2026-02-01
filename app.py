import streamlit as st
import google.generativeai as genai
from PIL import Image

st.title("🛡️ DocuDost: AI Auditor")

with st.sidebar:
    api_key = st.text_input("Gemini API Key", type="password")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    if st.button("Analyze"):
        try:
            genai.configure(api_key=api_key.strip())
            # Sabse zyada compatible name
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            response = model.generate_content(["Audit this in Hinglish", img])
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Bhai, ek baar 'aistudio.google.com' par jaakar 'Naya Project' bana kar key generate karo.")

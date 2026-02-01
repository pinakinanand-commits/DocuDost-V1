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
try:
            # Force the API to use v1 instead of v1beta
            genai.configure(api_key=api_key.strip())
            
            # Use 'models/gemini-1.5-flash' - full path likhna zaroori hai
            model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
            
            with st.spinner('DocuDost is auditing...'):
                # Content generation
                response = model.generate_content([
                    "Identify this legal document and list 3 potential risks in Hinglish.", 
                    img
                ])
                st.success("Analysis Complete!")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Error: {e}")            
            response = model.generate_content(["Audit this in Hinglish", img])
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Bhai, ek baar 'aistudio.google.com' par jaakar 'Naya Project' bana kar key generate karo.")

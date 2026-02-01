import streamlit as st
import google.generativeai as genai
from PIL import Image

st.title("🛡️ DocuDost: AI Legal Auditor")

api_key = st.sidebar.text_input("Gemini API Key", type="password")
uploaded_file = st.file_uploader("Upload Document", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    st.image(img, width=300)
    
    if st.button("Analyze"):
        try:
            genai.configure(api_key=api_key.strip())
            # Latest stable model
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner('Checking for risks...'):
                response = model.generate_content(["Identify document and list 3 risks in Hinglish", img])
                st.success("Done!")
                st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")

import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="DocuDost AI", page_icon="🛡️")
st.title("🛡️ DocuDost: AI Legal Auditor")

with st.sidebar:
    api_key = st.text_input("Enter Gemini API Key", type="password")

uploaded_file = st.file_uploader("Upload Document", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    st.image(img, caption="Document Loaded", width=300)
    
    if st.button("Analyze Now"):
        try:
            # 4 spaces ka gap zaroori hai try ke niche
            genai.configure(api_key=api_key.strip())
            
            # Model selection
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner('DocuDost is auditing...'):
                response = model.generate_content([
                    "Analyze this document and list 3 legal risks in Hinglish.", 
                    img
                ])
                st.success("Analysis Done!")
                st.markdown("### 📋 Audit Report")
                st.write(response.text)
                
        except Exception as e:
            # 4 spaces ka gap yahan bhi
            st.error(f"Error: {e}")
            st.info("Bhai, agar 404 aaye toh Google AI Studio mein Naya Project banao.")

elif not api_key and uploaded_file:
    st.warning("Please enter your API Key in the sidebar.")

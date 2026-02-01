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
            # Force setting the API key
            genai.configure(api_key=api_key.strip())
            
            # Use 'gemini-1.5-flash' - Is line ko dhyan se dekho
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner('DocuDost is auditing...'):
                # Note: Content generation
                response = model.generate_content([
                    "Analyze this document image. Identify document type and list 3 legal risks in Hinglish.", 
                    img
                ])
                st.success("Analysis Done!")
                st.markdown("### 📋 Audit Report")
                st.write(response.text)
                
        except Exception as e:
            # Detailed Error for debugging
            st.error(f"Technical Error: {str(e)}")

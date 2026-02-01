import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="DocuDost AI", page_icon="🛡️")
st.title("🛡️ DocuDost: AI Legal Auditor")

with st.sidebar:
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Make sure you updated requirements.txt first!")

uploaded_file = st.file_uploader("Upload Document Image", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    st.image(img, caption="Document Loaded", width=300)
    
    if st.button("Analyze Document"):
        try:
            # 1. Setup
            genai.configure(api_key=api_key.strip())
            
            # 2. Latest Model Name
            model = genai.GenerativeModel(model_name='gemini-1.5-flash')
            
            with st.spinner('AI is analyzing...'):
                # 3. Request
                response = model.generate_content([
                    "Analyze this document image and list 3 major risks in Hinglish.", 
                    img
                ])
                st.success("Analysis Complete!")
                st.markdown("### 📋 Audit Report")
                st.write(response.text)
                
        except Exception as e:
            # Yeh block missing hone se SyntaxError aata hai
            st.error(f"Technical Error: {e}")

elif not api_key and uploaded_file:
    st.warning("Please enter your API Key in the sidebar.")

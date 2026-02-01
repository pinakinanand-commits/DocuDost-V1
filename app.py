import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="DocuDost AI", page_icon="🛡️")
st.title("🛡️ DocuDost: AI Legal Auditor")

with st.sidebar:
    api_key = st.text_input("Enter Gemini API Key", type="password")

uploaded_file = st.file_uploader("Upload Document Image", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    st.image(img, caption="Document Loaded", width=300)
    
    if st.button("Analyze Document"):
        try:
            # Step 1: Configuration
            genai.configure(api_key=api_key.strip())
            
            # Step 2: Hum sabse stable naya model use kar rahe hain
            # 'gemini-1.5-flash' hi ab standard hai
        try:
            genai.configure(api_key=api_key.strip())
            # Hum system ko bol rahe hain 'models/gemini-1.5-flash' use kare
            model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
            
            with st.spinner('AI is reading your document...'):
                # Note: Content generation
                response = model.generate_content([
                    "Analyze this document image and list 3 major risks in Hinglish.", 
                    img
                ])
                st.success("Analysis Complete!")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Technical Error: {e}")            
            with st.spinner('AI is reading your document...'):
                # Image ko prompt ke saath bhejna
                response = model.generate_content([
                    "You are a legal expert. Identify this document and list 3 major risks in Hinglish.", 
                    img
                ])
                
                st.success("Analysis Complete!")
                st.markdown("### 📋 Audit Report")
                st.write(response.text)
                
        except Exception as e:
            # Agar abhi bhi error aaye, toh error message print hoga
            st.error(f"Error Message: {e}")
            st.info("Tip: Make sure you created the API key in 'Google AI Studio' and not Google Cloud Console.")

elif not api_key and uploaded_file:
    st.warning("Please enter your API Key in the sidebar.")

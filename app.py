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
    
    if st.button("Analyze Document"):
        try:
            genai.configure(api_key=api_key.strip())
            
            # Model testing list - Jo chal jaye wahi sahi!
            # Hum 'gemini-1.5-flash-latest' try karenge kyunki ye v1 par zyada stable hai
            model_names = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro-vision']
            
            response = None
            for m_name in model_names:
                try:
                    model = genai.GenerativeModel(m_name)
                    with st.spinner(f'Trying model: {m_name}...'):
                        response = model.generate_content([
                            "Analyze this document and list 3 legal risks in Hinglish.", 
                            img
                        ])
                        if response:
                            break
                except:
                    continue
            
            if response:
                st.success("Analysis Complete!")
                st.markdown("### 📋 Audit Report")
                st.write(response.text)
            else:
                st.error("Bhai, koi bhi model respond nahi kar raha. Check your Google AI Studio permissions.")
                
        except Exception as e:
            st.error(f"Error: {e}")

elif not api_key and uploaded_file:
    st.warning("Please enter your API Key.")

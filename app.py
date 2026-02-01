import streamlit as st
import requests
import base64
from PIL import Image
import io

# Page Configuration
st.set_page_config(page_title="DocuDost AI", page_icon="⚖️", layout="centered")

# Custom CSS for better looks
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #007bff; color: white; }
    .report-box { padding: 20px; border-radius: 10px; background-color: white; border-left: 5px solid #007bff; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ DocuDost: AI Legal Auditor")
st.write("Apne legal documents upload karein aur AI se risks jaaniye.")

# Sidebar for Settings
with st.sidebar:
    st.header("🔑 API Configuration")
    api_key = st.text_input("Enter OpenRouter API Key", type="password")
    st.info("Model: Llama-3.2 Vision (Stable)")
    st.markdown("---")
    st.write("Made with ❤️ by DocuDost Team")

# File Uploader
uploaded_file = st.file_uploader("Upload Document (Image)", type=["png", "jpg", "jpeg"])

def analyze_document(key, img_file):
    img_byte_arr = io.BytesIO()
    img_file.save(img_byte_arr, format='JPEG')
    img_b64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    
    # Updated Prompt for better Hinglish Analysis
    prompt = """Analyze this legal document image. 
    1. Identify what type of document it is.
    2. List 3-4 major legal risks or hidden points.
    Write the response in simple Hinglish (mixture of Hindi and English) so a common person can understand."""

    payload = {
        "model": "meta-llama/llama-3.2-11b-vision-instruct",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    return response.json()

# Main Logic
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Document Preview", use_container_width=True)
    
    if st.button("🔍 Start Legal Audit"):
        if not api_key:
            st.error("Bhai, pehle Sidebar mein API Key toh daalo!")
        else:
            with st.spinner("AI document padh raha hai... Thoda sabar rakhein."):
                try:
                    result = analyze_document(api_key, img)
                    
                    if 'choices' in result:
                        report = result['choices'][0]['message']['content']
                        st.success("✅ Audit Complete!")
                        st.markdown("### 📋 Legal Audit Report (Hinglish)")
                        st.markdown(f"<div class='report-box'>{report}</div>", unsafe_allow_html=True)
                        
                        # Download Button
                        st.download_button("Download Report", report, file_name="legal_audit.txt")
                    else:
                        st.error("Model busy ya key error. Dubara koshish karein.")
                        st.json(result)
                except Exception as e:
                    st.error(f"Connection Error: {e}")

else:
    st.info("Document upload karein audit shuru karne ke liye.")

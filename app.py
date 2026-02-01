import streamlit as st
import requests
import base64
from PIL import Image
import io

st.set_page_config(page_title="DocuDost AI", page_icon="⚖️")

# Styling for Red Highlights
st.markdown("""
    <style>
    .danger-zone { 
        color: #d9534f; 
        background-color: #f9f2f2; 
        padding: 10px; 
        border-radius: 5px; 
        border-left: 10px solid #d9534f;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .safe-zone {
        color: #5cb85c;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ DocuDost: AI Legal Auditor")

api_key = st.sidebar.text_input("Enter OpenRouter API Key", type="password")
uploaded_file = st.file_uploader("Upload Document Image", type=["png", "jpg", "jpeg"])

def analyze_document_v2(key, img_file):
    img_byte_arr = io.BytesIO()
    img_file.save(img_byte_arr, format='JPEG')
    img_b64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    
    # Updated Professional Prompt to avoid Safety Filter
    prompt = """Task: Conduct a professional legal document review.
    1. Identify the document type.
    2. Point out clauses that lack enforceability or have high risk.
    3. Format: Start every risky point with 'ALERT:' and write in Hinglish.
    Be objective and factual."""

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
        ],
        "temperature": 0.1 # Kam temperature se AI zyada stable chalta hai
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    st.image(img, width=400)
    
    if st.button("🔍 Perform Audit"):
        with st.spinner("AI is analyzing safely..."):
            result = analyze_document_v2(api_key, img)
            
            if 'choices' in result:
                text = result['choices'][0]['message']['content']
                
                # Logic to convert ALERT: into Red Boxes
                lines = text.split('\n')
                st.markdown("### 📋 Audit Results")
                for line in lines:
                    if "ALERT:" in line:
                        st.markdown(f"<div class='danger-zone'>{line}</div>", unsafe_allow_html=True)
                    else:
                        st.write(line)
            else:
                st.error("AI is refusing to read this document. Please try a clearer image.")
                st.json(result)

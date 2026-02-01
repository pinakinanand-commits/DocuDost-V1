import streamlit as st
import requests
import base64
from PIL import Image
import io

st.set_page_config(page_title="DocuDost AI", page_icon="⚖️")

# Styling for Red Box
st.markdown("""
    <style>
    .risk-alert { 
        color: white; 
        background-color: #d9534f; 
        padding: 15px; 
        border-radius: 8px; 
        font-weight: bold;
        margin-bottom: 10px;
        border: 2px solid #b52b27;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ DocuDost: AI Legal Auditor")

api_key = st.sidebar.text_input("Enter OpenRouter API Key", type="password")
uploaded_file = st.file_uploader("Upload Document Image", type=["png", "jpg", "jpeg"])

def analyze_document_v3(key, img_file):
    img_byte_arr = io.BytesIO()
    img_file.save(img_byte_arr, format='JPEG')
    img_b64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    
    # Model badal kar Gemini kar diya taaki 'Unsafe' error bypass ho jaye
    payload = {
        "model": "google/gemini-flash-1.5", 
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Identify document type and list 3 legal risks in Hinglish. Start every risk with the word 'KHATRA:'."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    st.image(img, width=400)
    
    if st.button("Final Audit"):
        with st.spinner("AI analyzing your document..."):
            result = analyze_document_v3(api_key, img)
            
            if 'choices' in result:
                text = result['choices'][0]['message']['content']
                st.markdown("### 📋 Audit Results")
                
                # Logic to find 'KHATRA:' and show it in RED
                lines = text.split('\n')
                for line in lines:
                    if "KHATRA:" in line or "RISK:" in line:
                        st.markdown(f"<div class='risk-alert'>⚠️ {line}</div>", unsafe_allow_html=True)
                    else:
                        st.write(line)
            else:
                st.error("Error: AI is still blocking this. Try a new OpenRouter Key.")
                st.json(result)

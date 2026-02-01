import streamlit as st
import requests
import base64
from PIL import Image
import io

st.set_page_config(page_title="DocuDost AI", page_icon="⚖️")

# Custom Red Highlight CSS
st.markdown("""
    <style>
    .danger-alert { 
        color: white; 
        background-color: #ff4d4d; 
        padding: 12px; 
        border-radius: 8px; 
        font-weight: bold;
        margin-top: 5px;
        border-left: 8px solid #b30000;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ DocuDost: AI Legal Auditor")

api_key = st.sidebar.text_input("Enter OpenRouter API Key", type="password")
uploaded_file = st.file_uploader("Upload Document Image", type=["png", "jpg", "jpeg"])

def call_ai(key, img_b64, model_name):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this document and list 3 legal risks in Hinglish. Start every risky point with 'KHATRA:'"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=40)
        return response.json()
    except:
        return None

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    st.image(img, width=400)
    
    if st.button("Start Professional Audit"):
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_b64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

        # Best models for Vision in 2026 on OpenRouter
        models = [
            "google/gemini-pro-1.5", 
            "openai/gpt-4o-mini",
            "meta-llama/llama-3.2-11b-vision-instruct"
        ]
        
        found = False
        for m in models:
            with st.spinner(f"Trying Model: {m}..."):
                result = call_ai(api_key, img_b64, m)
                if result and 'choices' in result:
                    report = result['choices'][0]['message']['content']
                    st.success(f"Audit Complete using {m}!")
                    
                    # Formatting logic for Red Boxes
                    lines = report.split('\n')
                    for line in lines:
                        if "KHATRA:" in line or "RISK:" in line or "ALERT:" in line:
                            st.markdown(f"<div class='danger-alert'>⚠️ {line}</div>", unsafe_allow_html=True)
                        else:
                            st.write(line)
                    found = True
                    break
        
        if not found:
            st.error("Bhai, OpenRouter ke saare models abhi nakhre kar rahe hain. Ek baar apna OpenRouter balance check karein (Credits zero toh nahi?)")
            if result: st.json(result)

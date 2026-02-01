import streamlit as st
import requests
import base64
from PIL import Image
import io

st.set_page_config(page_title="DocuDost AI", page_icon="⚖️")

# Custom CSS for Red Highlights
st.markdown("""
    <style>
    .risk-text { color: #ff4b4b; font-weight: bold; background-color: #ffe8e8; padding: 5px; border-radius: 5px; }
    .main-box { padding: 20px; border-radius: 10px; background-color: #ffffff; box-shadow: 0px 4px 12px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ DocuDost: AI Legal Auditor")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter OpenRouter API Key", type="password")

uploaded_file = st.file_uploader("Upload Document", type=["png", "jpg", "jpeg"])

def analyze_document(key, img_file):
    img_byte_arr = io.BytesIO()
    img_file.save(img_byte_arr, format='JPEG')
    img_b64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    
    # AI ko instruction ki wo galat points ko red mark kare
    prompt = """Analyze this document. 
    1. List 3 major legal risks in Hinglish.
    2. Format the response such that every negative or dangerous point starts with '⚠️ RISK:'.
    3. Use simple language."""

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
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    st.image(img, width=400)
    
    if st.button("Analyze & Highlight Risks"):
        with st.spinner("AI scan kar raha hai..."):
            result = analyze_document(api_key, img)
            if 'choices' in result:
                full_text = result['choices'][0]['message']['content']
                
                # Logic: Jahan 'RISK:' likha ho wahan color red kar do
                formatted_text = full_text.replace("RISK:", " <span class='risk-text'>RISK:</span>")
                
                st.markdown("### 📋 Audit Results")
                st.markdown(f"<div class='main-box'>{formatted_text}</div>", unsafe_allow_html=True)
            else:
                st.error("Kuch problem aayi hai. Dashboard check karein.")

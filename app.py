import streamlit as st
import requests
import base64
from PIL import Image
import io

st.set_page_config(page_title="DocuDost AI", page_icon="🛡️")
st.title("🛡️ DocuDost: AI Legal Auditor")

api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
uploaded_file = st.file_uploader("Upload Document", type=["png", "jpg", "jpeg"])

def try_analyze(key, img_b64, model_name):
    # Try with both v1 and v1beta automatically
    for version in ["v1", "v1beta"]:
        url = f"https://generativelanguage.googleapis.com/{version}/models/{model_name}:generateContent?key={key}"
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Analyze this document and list 3 legal risks in Hinglish."},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
                ]
            }]
        }
        response = requests.post(url, json=payload)
        res_json = response.json()
        if 'candidates' in res_json:
            return res_json['candidates'][0]['content']['parts'][0]['text']
    return None

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    st.image(img, width=300)
    
    if st.button("Start Final Audit"):
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_b64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

        # List of all possible models in 2026
        models_to_try = ["gemini-1.5-flash", "gemini-1.5-flash-8b", "gemini-1.5-pro"]
        
        success = False
        for m in models_to_try:
            with st.spinner(f"Trying Model: {m}..."):
                report = try_analyze(api_key, img_b64, m)
                if report:
                    st.success(f"Success! (Used: {m})")
                    st.write(report)
                    success = True
                    break
        
        if not success:
            st.error("Bhai, Google ke saare raste band hain. Ek baar 'Google AI Studio' mein jaakar naya API Key generate karein.")

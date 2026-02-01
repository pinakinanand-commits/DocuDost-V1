import streamlit as st
import requests
import base64
from PIL import Image
import io

st.set_page_config(page_title="DocuDost AI", page_icon="🛡️")
st.title("🛡️ DocuDost: AI Legal Auditor (Stable)")

api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
uploaded_file = st.file_uploader("Upload Document", type=["png", "jpg", "jpeg"])

def analyze_image(api_key, image_file):
    # Image ko AI ke samajhne layak format (base64) mein badalna
    img_byte_arr = io.BytesIO()
    image_file.save(img_byte_arr, format='JPEG')
    img_b64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

    # Seedha Google ke Stable API endpoint par hit karna
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [
                {"text": "Analyze this document and list 3 legal risks in Hinglish."},
                {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
            ]
        }]
    }
    
    response = requests.post(url, json=payload)
    return response.json()

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    st.image(img, width=300)
    
    if st.button("Analyze Now"):
        with st.spinner("AI processing..."):
            result = analyze_image(api_key, img)
            
            if 'candidates' in result:
                report = result['candidates'][0]['content']['parts'][0]['text']
                st.success("Analysis Done!")
                st.write(report)
            else:
                st.error(f"Error: {result.get('error', {}).get('message', 'Unknown Error')}")

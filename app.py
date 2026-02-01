import streamlit as st
import requests
import base64
from PIL import Image
import io

st.set_page_config(page_title="DocuDost AI", page_icon="🛡️")
st.title("🛡️ DocuDost: AI Legal Auditor")

api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
uploaded_file = st.file_uploader("Upload Document", type=["png", "jpg", "jpeg"])

def analyze_document_direct(key, img_file):
    img_byte_arr = io.BytesIO()
    img_file.save(img_byte_arr, format='JPEG')
    img_b64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

    # YAHAN BADLAV HAI: 'v1' ki jagah 'v1beta' use kar rahe hain
    # Kyunki aapka account isi version par model support kar raha hai
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [
                {"text": "Analyze this document and list 3 legal risks in Hinglish. Be very simple."},
                {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
            ]
        }]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    st.image(img, width=300)
    
    if st.button("Start Audit"):
        with st.spinner("Connecting to Secure Server..."):
            result = analyze_document_direct(api_key, img)
            
            if 'candidates' in result:
                text = result['candidates'][0]['content']['parts'][0]['text']
                st.success("Analysis Complete!")
                st.write(text)
            else:
                st.error("Model Error")
                st.json(result) # Isse final check ho jayega

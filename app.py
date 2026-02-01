import streamlit as st
import requests
import base64
from PIL import Image
import io

st.set_page_config(page_title="DocuDost AI", page_icon="🛡️")
st.title("🛡️ DocuDost: AI Legal Auditor (Stable Mode)")

# Sidebar for OpenRouter Key
api_key = st.sidebar.text_input("Enter OpenRouter API Key", type="password")
uploaded_file = st.file_uploader("Upload Document", type=["png", "jpg", "jpeg"])

def analyze_document_openrouter(key, img_file):
    img_byte_arr = io.BytesIO()
    img_file.save(img_byte_arr, format='JPEG')
    img_b64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

    # OpenRouter API Endpoint (Sabse Stable)
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "meta-llama/llama-3.2-11b-vision-instruct:free", # FREE MODEL
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this document and list 3 legal risks in Hinglish."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}
                    }
                ]
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    st.image(img, width=300)
    
    if st.button("Final Analysis"):
        with st.spinner("Analyzing via Llama-3 (Stable)..."):
            result = analyze_document_openrouter(api_key, img)
            
            if 'choices' in result:
                text = result['choices'][0]['message']['content']
                st.success("Bhai, Ho Gaya! Report dekho:")
                st.write(text)
            else:
                st.error("Error Detail:")
                st.json(result)

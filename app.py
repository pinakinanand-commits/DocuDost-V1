import streamlit as st
import requests
import base64
from PIL import Image
import io

st.set_page_config(page_title="DocuDost AI", page_icon="🛡️")
st.title("🛡️ DocuDost: AI Legal Auditor")

api_key = st.sidebar.text_input("Enter OpenRouter API Key", type="password")
uploaded_file = st.file_uploader("Upload Document", type=["png", "jpg", "jpeg"])

def analyze_document_final(key, img_file):
    img_byte_arr = io.BytesIO()
    img_file.save(img_byte_arr, format='JPEG')
    img_b64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501", # Streamlit local referer
        "X-Title": "DocuDost AI"
    }
    
    payload = {
        # YEH MODEL NAME SABSE STABLE HAI OPENROUTER PAR
        "model": "google/gemini-flash-1.5", 
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this legal document and list 3 risks in Hinglish."},
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
    
    if st.button("Run Audit"):
        with st.spinner("Connecting to OpenRouter..."):
            result = analyze_document_final(api_key, img)
            
            if 'choices' in result:
                text = result['choices'][0]['message']['content']
                st.success("Analysis Complete!")
                st.write(text)
            else:
                st.error("Model Error")
                st.json(result) # Isse exact model name pata chal jayega

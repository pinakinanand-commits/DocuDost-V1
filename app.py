import streamlit as st
import requests
import base64
from PIL import Image
import io

st.set_page_config(page_title="DocuDost AI", page_icon="🛡️")
st.title("🛡️ DocuDost: AI Legal Auditor")

api_key = st.sidebar.text_input("Enter OpenRouter API Key", type="password")
uploaded_file = st.file_uploader("Upload Document", type=["png", "jpg", "jpeg"])

def call_openrouter(key, img_b64, model_name):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "DocuDost"
    }
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this document and list 3 legal risks in Hinglish."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    st.image(img, width=300)
    
    if st.button("Start Final Audit"):
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_b64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

        # List of models currently active on OpenRouter (2026 names)
        # Inhe ek-ek karke try karega
        models_to_test = [
            "google/gemini-flash-1.5-8b", 
            "google/gemini-2.0-flash-exp:free",
            "meta-llama/llama-3.2-11b-vision-instruct",
            "google/gemini-flash-1.5"
        ]
        
        success = False
        for m in models_to_test:
            with st.spinner(f"Trying Model: {m}..."):
                result = call_openrouter(api_key, img_b64, m)
                if 'choices' in result:
                    st.success(f"Bhai, Ho Gaya! (Model: {m})")
                    st.write(result['choices'][0]['message']['content'])
                    success = True
                    break
        
        if not success:
            st.error("Bhai, OpenRouter par koi Vision model response nahi de raha.")
            st.json(result) # Taki humein exact error dikhe

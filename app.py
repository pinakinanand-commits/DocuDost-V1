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
    }
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this document and list 3 legal risks in Hinglish. Be quick!"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            }
        ]
    }
    # Timeout 30 seconds ka taaki 'goom goom' na hota rahe
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    return response.json()

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    st.image(img, width=300)
    
    if st.button("Instant Audit"):
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_b64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

        # 2026 ka sabse fast model jo OpenRouter par FREE hai
        fast_model = "google/gemini-2.0-flash-exp:free"
        
        with st.spinner(f"Processing with {fast_model}..."):
            try:
                result = call_openrouter(api_key, img_b64, fast_model)
                if 'choices' in result:
                    st.success("Analysis Complete!")
                    st.write(result['choices'][0]['message']['content'])
                else:
                    st.error("Model busy, trying fallback...")
                    # Agar pehla fail ho toh Llama try karein
                    result_fallback = call_openrouter(api_key, img_b64, "meta-llama/llama-3.2-11b-vision-instruct")
                    st.write(result_fallback['choices'][0]['message']['content'])
            except Exception as e:
                st.error(f"Slow connection: {e}")

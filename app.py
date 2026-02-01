import streamlit as st
import requests
import base64
from PIL import Image
import io

st.set_page_config(page_title="DocuDost AI Pro", page_icon="⚖️", layout="wide")

# Stylish CSS
st.markdown("""
    <style>
    .danger-alert { color: white; background-color: #ff4d4d; padding: 15px; border-radius: 10px; font-weight: bold; border-left: 10px solid #b30000; margin-bottom: 10px; }
    .advice-box { background-color: #e3f2fd; border: 1px solid #2196f3; padding: 15px; border-radius: 10px; color: #0d47a1; }
    .stButton>button { border-radius: 50px; background-color: #007bff; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ DocuDost AI: Legal Auditor Pro")

with st.sidebar:
    st.header("⚙️ Control Panel")
    api_key = st.text_input("Enter OpenRouter API Key", type="password")
    st.info("Supported: JPG, PNG, JPEG")
    st.warning("Note: PDF support ke liye image scan use karein.")

uploaded_file = st.file_uploader("Upload Document (Photo)", type=["png", "jpg", "jpeg"])

def call_audit_ai(key, img_b64):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    
    # Prompt for Risks + Legal Advice
    prompt = """Analyze this legal document:
    1. Summarize it in 2 lines.
    2. List 3 major 'KHATRA:' (Risks) in Hinglish.
    3. Provide 'LEGAL ADVICE:' in Hinglish on what the user should do next.
    Make it professional yet easy."""

    payload = {
        "model": "openai/gpt-4o-mini", # Sabse stable model
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
    col1, col2 = st.columns([1, 1])
    
    with col1:
        img = Image.open(uploaded_file)
        st.image(img, caption="Document Preview", use_container_width=True)
    
    with col2:
        if st.button("🚀 Start Deep Audit"):
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_b64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

            with st.spinner("AI Legal Mind working..."):
                result = call_audit_ai(api_key, img_b64)
                
                if 'choices' in result:
                    report = result['choices'][0]['message']['content']
                    st.markdown("### 📋 Professional Audit Report")
                    
                    # Logic to highlight Risks and Advice
                    lines = report.split('\n')
                    for line in lines:
                        if "KHATRA:" in line:
                            st.markdown(f"<div class='danger-alert'>⚠️ {line}</div>", unsafe_allow_html=True)
                        elif "LEGAL ADVICE:" in line:
                            st.markdown(f"<div class='advice-box'>💡 {line}</div>", unsafe_allow_html=True)
                        else:
                            st.write(line)
                else:
                    st.error("Error in Analysis. Check API Balance.")

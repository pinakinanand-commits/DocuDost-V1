import streamlit as st
import requests
import base64
from PIL import Image
import io

# Page Config
st.set_page_config(page_title="DocuDost Pro", page_icon="⚖️")

# CSS for styling
st.markdown("""
    <style>
    .risk-box { color: white; background-color: #d9534f; padding: 12px; border-radius: 8px; font-weight: bold; margin-bottom: 8px; border-left: 5px solid #b30000; }
    .advice-box { background-color: #e3f2fd; border: 1px solid #2196f3; padding: 12px; border-radius: 8px; color: #0d47a1; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ DocuDost: Secure Legal Auditor")

# --- ADMIN PASSWORD LOCK ---
# Ab ye Admin Password bhi secrets se uthayega
PASSWORD = st.secrets["APP_PASSWORD"]
with st.sidebar:
    st.header("🔒 Access Control")
    user_pass = st.text_input("Enter Access Password", type="password")
    st.info("Bhai, bina password ke audit nahi chalega!")

# --- GET API KEY FROM SECRETS ---
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except:
    st.error("Error: Streamlit Secrets mein API Key missing hai!")
    st.stop()

uploaded_file = st.file_uploader("Upload Document (Image)", type=["png", "jpg", "jpeg"])

def analyze_document(key, img_obj):
    img_byte_arr = io.BytesIO()
    # Yahan img_obj already Image.open() se pass ho raha hai
    img_obj.convert('RGB').save(img_byte_arr, format='JPEG')
    img_b64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze document. List 3 'KHATRA:' and 1 'LEGAL ADVICE:' in Hinglish."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# --- MAIN LOGIC ---
if uploaded_file:
    # Image load kar rahe hain display aur process ke liye
    image_to_show = Image.open(uploaded_file)
    st.image(image_to_show, width=300)
    
    if st.button("Start Audit"):
        if user_pass != PASSWORD:
            st.error("Ghalat Password! Bhai, sahi password daalo.")
        else:
            with st.spinner("AI is auditing..."):
                # Analyze function ko call kar rahe hain
                result = analyze_document(api_key, image_to_show)
                
                if result and 'choices' in result:
                    report = result['choices'][0]['message']['content']
                    st.markdown("### 📋 Final Report")
                    
                    lines = report.split('\n')
                    for line in lines:
                        if "KHATRA:" in line:
                            st.markdown(f"<div class='risk-box'>⚠️ {line}</div>", unsafe_allow_html=True)
                        elif "LEGAL ADVICE:" in line:
                            st.markdown(f"<div class='advice-box'>💡 {line}</div>", unsafe_allow_html=True)
                        else:
                            st.write(line)
                else:
                    st.error("API Error. Check OpenRouter balance or Secrets.")

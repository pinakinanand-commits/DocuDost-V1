import streamlit as st
import requests
import base64
from PIL import Image
import io

# Page Configuration
st.set_page_config(page_title="DocuDost AI", page_icon="⚖️", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .risk-card { color: white; background-color: #ff4d4d; padding: 15px; border-radius: 12px; font-weight: bold; margin-bottom: 10px; border-left: 10px solid #b30000; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    .advice-card { background-color: #e3f2fd; border-left: 10px solid #2196f3; padding: 15px; border-radius: 12px; color: #0d47a1; margin-top: 15px; }
    .trust-box { background-color: #f8f9fa; border: 1px dashed #6c757d; padding: 20px; border-radius: 15px; text-align: center; margin-top: 30px; color: #495057; }
    .stButton>button { width: 100%; border-radius: 25px; height: 3.5em; background-image: linear-gradient(to right, #007bff, #0056b3); color: white; border: none; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ DocuDost: AI Document Auditor")
st.write("Apne legal documents ko scan karein aur risks ko seconds mein samjhein.")

# Sidebar for Access
with st.sidebar:
    st.header("🔒 Access Control")
    # Secrets se uthayega password aur API key
    try:
        ADMIN_PASSWORD = st.secrets["APP_PASSWORD"]
        api_key = st.secrets["OPENROUTER_API_KEY"]
    except:
        st.error("Secrets not set! Check Streamlit Dashboard.")
        st.stop()
        
    user_pass = st.text_input("Enter Access Password", type="password")

# File Upload Section
uploaded_file = st.file_uploader("Upload Document (Photo)", type=["png", "jpg", "jpeg"])

def analyze_doc(key, img_obj):
    img_byte_arr = io.BytesIO()
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
                    {"type": "text", "text": "Analyze this legal doc. List 3 'KHATRA:' (risks) and 1 'SUGGESTION:' in Hinglish. Be very clear."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

if uploaded_file:
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        img_preview = Image.open(uploaded_file)
        st.image(img_preview, caption="Your Document", use_container_width=True)
    
    with col2:
        if st.button("🔍 Analyze Document Now"):
            if user_pass != ADMIN_PASSWORD:
                st.error("Galat Password! Please try again.")
            else:
                with st.spinner("AI is reading your document..."):
                    result = analyze_doc(api_key, img_preview)
                    if 'choices' in result:
                        report = result['choices'][0]['message']['content']
                        st.subheader("📋 Audit Report")
                        
                        lines = report.split('\n')
                        for line in lines:
                            if "KHATRA:" in line:
                                st.markdown(f"<div class='risk-card'>⚠️ {line}</div>", unsafe_allow_html=True)
                            elif "SUGGESTION:" in line:
                                st.markdown(f"<div class='advice-card'>💡 {line}</div>", unsafe_allow_html=True)
                            else:
                                st.write(line)
                                
                        # --- THE SMART TRUST BOX (No Scare, Only Trust) ---
                        st.markdown("""
                            <div class='trust-box'>
                                <b>✨ DocuDost Tip:</b> Ye AI report aapki help ke liye hai. 
                                Ek final legal advice ke liye aap apne trusted Lawyer se consult kar sakte hain. 
                                Humara maksad aapka kaam 10x asaan karna hai!
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("Analysis failed. Check credits.")

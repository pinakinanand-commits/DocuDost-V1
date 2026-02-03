import streamlit as st
import requests
import base64
from PIL import Image
import io

# 1. Page Configuration
st.set_page_config(page_title="DocuDost AI", page_icon="⚖️", layout="wide")

# 2. Custom CSS for Premium Design
st.markdown("""
    <style>
    .risk-card { color: white; background-color: #ff4d4d; padding: 15px; border-radius: 12px; font-weight: bold; margin-bottom: 10px; border-left: 10px solid #b30000; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    .advice-card { background-color: #e3f2fd; border-left: 10px solid #2196f3; padding: 15px; border-radius: 12px; color: #0d47a1; margin-top: 15px; }
    .trust-box { background-color: #f8f9fa; border: 1px dashed #6c757d; padding: 20px; border-radius: 15px; text-align: center; margin-top: 30px; color: #495057; }
    .stButton>button { width: 100%; border-radius: 25px; height: 3.5em; background-image: linear-gradient(to right, #007bff, #0056b3); color: white; border: none; font-size: 18px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER SECTION (Title & Tagline)
st.title("🛡️ DocuDost AI")
st.markdown("<h5 style='color: #6c757d; font-style: italic; margin-top: -20px; font-weight: 400;'>Your silent drafting partner.</h5>", unsafe_allow_html=True)
st.write("---")

# 4. SIDEBAR ACCESS
with st.sidebar:
    st.header("🔒 Access Control")
    try:
        ADMIN_PASSWORD = st.secrets["APP_PASSWORD"]
        api_key = st.secrets["OPENROUTER_API_KEY"]
    except:
        st.error("Secrets missing! Please set them in Streamlit Dashboard.")
        st.stop()
        
    user_pass = st.text_input("Enter Access Password", type="password")
    # --- SIDEBAR ACCESS (Line 30-45 ke aas paas) ---
with st.sidebar:
    st.header("🔒 Access Control")
    try:
        ADMIN_PASSWORD = st.secrets["APP_PASSWORD"]
        api_key = st.secrets["OPENROUTER_API_KEY"]
    except:
        st.error("Secrets missing! Please set them in Streamlit Dashboard.")
        st.stop()
        
    user_pass = st.text_input("Enter Access Password", type="password")

    # --- YAHAN ADD KAREIN PRICING SECTION ---
    st.markdown("---")
    st.subheader("💎 Future Plans")
    plan = st.radio("Select Plan:", ["Basic (Free)", "Standard (₹99)", "Professional (Full Access)"])
    
    if plan == "Standard (₹99)":
        st.info("Coming Soon: 50 pages per month for just ₹99!")
    elif plan == "Professional (Full Access)":
        st.info("Coming Soon: Unlimited audits for power users.")
    else:
        st.success("Beta Phase: Currently 1 page daily is FREE!")
    
    st.markdown("---")
    st.info("Bhai, ye app aapka 'Silent Partner' hai, aapka data safe hai.")
    st.markdown("---")
    st.info("Bhai, ye app aapka 'Silent Partner' hai, aapka data safe hai.")

# 5. MAIN LOGIC (File Upload)
uploaded_file = st.file_uploader("Upload Legal Document (Photo)", type=["png", "jpg", "jpeg"])

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
                    {"type": "text", "text": "Analyze this legal doc. List 3 'KHATRA:' (risks) and 1 'SUGGESTION:' in Hinglish. Be professional and clear."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# 6. APP EXECUTION
if uploaded_file:
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        img_preview = Image.open(uploaded_file)
        st.image(img_preview, caption="Document Scan", use_container_width=True)
    
    with col2:
        if st.button("🔍 Analyze Document Now"):
            if user_pass != ADMIN_PASSWORD:
                st.error("Galat Password! Sahi password daalein.")
            else:
                with st.spinner("DocuDost AI is working silently..."):
                    result = analyze_doc(api_key, img_preview)
                    if 'choices' in result:
                        report = result['choices'][0]['message']['content']
                        st.subheader("📋 Professional Audit Report")
                        
                        lines = report.split('\n')
                        for line in lines:
                            if "KHATRA:" in line:
                                st.markdown(f"<div class='risk-card'>⚠️ {line}</div>", unsafe_allow_html=True)
                            elif "SUGGESTION:" in line:
                                st.markdown(f"<div class='advice-card'>💡 {line}</div>", unsafe_allow_html=True)
                            else:
                                st.write(line)
                                
                        st.markdown("""
                            <div class='trust-box'>
                                <b>✨ DocuDost Tip:</b> Ye audit aapki help ke liye hai. 
                                Ek final legal check ke liye vakeel se consult karna hamesha behtar hota hai.
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("Analysis failed. API key ya balance check karein.")

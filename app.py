import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io

st.set_page_config(page_title="DocuDost AI", page_icon="🛡️")
st.title("🛡️ DocuDost: AI Legal Auditor")

with st.sidebar:
    st.header("Setup")
    api_key = st.text_input("Enter Groq API Key", type="password")
    st.markdown("[Get Free Key Here](https://console.groq.com/keys)")

uploaded_file = st.file_uploader("Upload Document (Image)", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Document Loaded", width=300)
    
    if st.button("Analyze Document"):
        try:
            client = Groq(api_key=api_key)
            
            # Image encoding
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

            with st.spinner('Latest Llama Vision model se scan ho raha hai...'):
                # TRYING THE MOST RECENT STABLE VISION MODEL
                # Note: If 11b and 90b are out, Llama-3.2-11b-vision-preview (updated) is usually the replacement
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Analyze this legal document and list 3 major risks in Hinglish."},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                                },
                            ],
                        }
                    ],
                    model="llama-3.2-11b-vision-preview", 
                )
                
                st.success("Analysis Complete!")
                st.markdown("### 📋 Audit Report")
                st.write(chat_completion.choices[0].message.content)
                
        except Exception as e:
            st.error(f"Model Error: {e}")
            st.info("Bhai, Groq ke 'Playground' mein dropdown check karo ki abhi 'Vision' ke liye kaunsa model active hai.")

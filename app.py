import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io

st.set_page_config(page_title="DocuDost AI", page_icon="🛡️")
st.title("🛡️ DocuDost: AI Legal Auditor")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Groq API Key", type="password")
    # Yahan wo naam likhein jo aapne Groq console par dekha
    model_choice = st.text_input("Model Name", value="llama-3.2-11b-vision-preview")

uploaded_file = st.file_uploader("Upload Document (Image)", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Document Loaded", width=300)
    
    if st.button("Analyze Document"):
        try:
            client = Groq(api_key=api_key)
            
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

            with st.spinner('Scanning...'):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Analyze this document and list 3 legal risks in Hinglish."},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                                }
                            ],
                        }
                    ],
                    model=model_choice, 
                )
                
                st.success("Success!")
                st.write(chat_completion.choices[0].message.content)
                
        except Exception as e:
            st.error(f"Error: {e}")

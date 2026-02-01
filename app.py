import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io

st.set_page_config(page_title="DocuDost AI", page_icon="🛡️")
st.title("🛡️ DocuDost: AI Legal Auditor")

# Sidebar mein Groq key maangein
with st.sidebar:
    st.header("Setup")
    api_key = st.text_input("Enter Groq API Key", type="password")
    st.markdown("[Get Free Key Here](https://console.groq.com/keys)")

uploaded_file = st.file_uploader("Upload Document (Image)", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    # Image process karna
    image = Image.open(uploaded_file)
    st.image(image, caption="Document Loaded", width=300)
    
    if st.button("Analyze with Llama-3"):
        try:
            client = Groq(api_key=api_key)
            
            # Image ko base64 format mein badalna (Groq isi ko samajhta hai)
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

            with st.spinner('Llama AI analysis kar raha hai...'):
                # Groq ka Vision model use karna
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Analyze this legal document and list 3 major risks in Hinglish. Be professional."},
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
            st.error(f"Error: {e}")

elif not api_key and uploaded_file:
    st.warning("Please enter your Groq API Key in the sidebar.")

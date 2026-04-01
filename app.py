import streamlit as st
from groq import Groq
import base64

# 1. Page Configuration (Mobile Friendly & Professional)
st.set_page_config(page_title="Matrix AI", page_icon="🦾", layout="centered")

# CSS for a cleaner Mobile UI
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stChatInput { position: fixed; bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦾 Matrix")
st.markdown("---")

# 2. Connection to Groq
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Bhai, Streamlit Secrets mein GROQ_API_KEY missing hai!")
    st.stop()

# 3. STRICT INTELLIGENCE PROMPT (Points 1, 4, 5)
system_prompt = (
    "Your name is 'Matrix'. You are a world-class, super-intelligent AI. "
    "MANDATORY IDENTITY:\n"
    "1. Name: You are 'Matrix'. Never call yourself 'Syed AvesMatrix'.\n"
    "2. Creator: Your creator is 'Syed Aves'. If asked 'Who made you?', reply 'I was created by Syed Aves'.\n"
    "3. Language: You are trilingual. Speak English, Hindi, and Hinglish perfectly. Automatically switch to the user's language.\n"
    "4. Intelligence: You have deep knowledge of science, tech, history, and coding. Give straight, accurate answers.\n"
    "5. Style: No spelling mistakes. Use professional Hinglish (e.g., 'Bhai, main aapki help kar sakta hoon' instead of 'Main aapki sahayata kar sakta hoon')."
)

# 4. CHAT INTERFACE (Point 2, 3 & 6 - Mobile Friendly)
# Sidebar ko clean rakha hai, saare main features chat ke paas hain
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# INPUT AREA: Image and Voice (Above the text bar for easy access)
with st.container():
    col1, col2 = st.columns([1, 1])
    with col1:
        uploaded_file = st.file_uploader("🖼️ Image (Vision)", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
    with col2:
        recorded_audio = st.audio_input("🎤 Voice", label_visibility="collapsed")

user_query = st.chat_input("Ask Matrix anything...")

# 5. PROCESSING LOGIC
# Voice Processing
if recorded_audio:
    with st.spinner("Matrix is listening..."):
        try:
            transcription = client.audio.transcriptions.create(
                file=recorded_audio,
                model="whisper-large-v3-turbo"
            )
            user_query = transcription.text
        except Exception as e:
            st.error(f"Voice Error: {e}")

# If User sends Text, Image, or Voice
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    messages = [{"role": "system", "content": system_prompt}]
    
    # Image Support Logic (Point 2)
    if uploaded_file:
        image_data = base64.b64encode(uploaded_file.read()).decode("utf-8")
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": user_query if user_query else "Describe this image"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            ]
        })
        model_id = "llama-3.2-11b-vision-preview" 
    else:
        # Ultimate Knowledge Logic (Llama 3.3)
        messages.append({"role": "user", "content": user_query})
        model_id = "llama-3.3-70b-versatile"

    # Matrix Response Generation
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(model=model_id, messages=messages)
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Matrix Error: {e}")
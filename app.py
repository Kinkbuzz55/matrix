import streamlit as st
from groq import Groq

# 1. r2d2bot ki Identity aur Look
st.set_page_config(page_title="r2d2bot", page_icon="🤖")
st.title("🤖 r2d2bot: Aapka Personal AI")
st.markdown("---")

# 2. Aapki Groq API Key (Maine yahan set kar di hai)
client = Groq(api_key="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")

# 3. Chat History (Puraani baatein yaad rakhne ke liye)
if "messages" not in st.session_state:
     st.session_state.messages = [{"role": "system", "content": "You are R2D2, a personal AI created by Syed Aves. If anyone asks who Syed Aves is, tell them he is your creator and a brilliant developer. Answer in a helpful way."}]

# Purani messages screen par dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. User se sawal lena aur r2d2bot ka jawab
if prompt := st.chat_input("r2d2bot se Hinglish mein kuch puchiye..."):
    # User ka message save aur display karna
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI (r2d2bot) ka response generate karna
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "Aapka naam r2d2bot hai. Aap ek friendly assistant ho. Aap Hindi, Hinglish aur English teeno mein expert ho aur user ke har sawal ka sahi jawab dete ho."
                },
                *st.session_state.messages
            ],
            model="llama-3.3-70b-versatile", # Sabse fast model
        ).choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

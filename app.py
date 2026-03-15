import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="kutiAİ v11.0", page_icon="🤖", layout="wide")

with st.sidebar:
    st.title("🎮 Eğlence")
    if st.button("🚀 Flappy Bird Başlat"):
        st.info("Oyun çok yakında buraya eklenecek!")
    
    st.divider()
    if st.button("🗑️ Hafızayı Temizle"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 kutiAİ v11.0")

# API Key'i gizli yerden (Secrets) alıyoruz ki ban yemeyesin
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-pro") 
else:
    st.error("🔑 API Key bulunamadı! Ayarlardan Secrets kısmına ekle.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"⚠️ Hata: {str(e)}")

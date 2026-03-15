import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="KutiAİ v11.0", page_icon="🤖", layout="wide")

# Sol Menü (Sidebar)
with st.sidebar:
    st.title("🎮 Eğlence")
    if st.button("🚀 Flappy Bird Başlat"):
        st.info("Oyun çok yakında buraya eklenecek!")
    
    st.divider()
    if st.button("🗑️ Hafızayı Temizle"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 kutiAİ v11.0")

# API Anahtarı Kontrolü (Streamlit Secrets üzerinden)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # En sağlam çalışan model ismi
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.error("🔑 API Key bulunamadı! Lütfen Streamlit Settings > Secrets kısmına anahtarınızı ekleyin.")
    st.stop()

# Sohbet Geçmişi Başlatma
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları Ekranda Göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan Giriş Al
if prompt := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            full_response = response.text
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"⚠️ Bir hata oluştu: {str(e)}")

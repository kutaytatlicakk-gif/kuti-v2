import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="KutiAİ VIP Asistan", page_icon="🤖", layout="wide")

# Sol Menü
with st.sidebar:
    st.title("⚙️ Kontrol Paneli")
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.markdown("🚀 **KutiAİ v1.1**")
    st.markdown("Geliştirici: Kutay")

st.title("🤖 KutiAİ VIP Asistan")
st.caption("En güncel sürüm ile güçlendirildi")

# API Anahtarını Secrets'tan çek
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # BURASI ÇOK ÖNEMLİ: Başına 'models/' ekledik, bu hatayı çözecek
    model = genai.GenerativeModel("models/gemini-1.5-flash")
else:
    st.error("🔑 API Key bulunamadı! Lütfen Secrets kısmına ekleyin.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("KutiAİ'ye bir şeyler sorun..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Hata mesajını daha anlaşılır yaptık
            st.error(f"Bir hata oluştu: {str(e)}")

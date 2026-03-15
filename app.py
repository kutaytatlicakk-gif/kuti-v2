import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="KutiAİ VIP", page_icon="🤖")
st.title("🤖 KutiAİ VIP Asistan")

# Şifreyi Streamlit Secrets'tan alıyoruz
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # GARANTİ MODEL İSMİ:
    model = genai.GenerativeModel("models/gemini-1.5-flash")
else:
    st.error("🔑 API Key Sırlar (Secrets) kısmında bulunamadı!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if p := st.chat_input("Mesajını yaz..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)
    with st.chat_message("assistant"):
        try:
            # Burası artık hata vermemeli
            r = model.generate_content(p)
            st.markdown(r.text)
            st.session_state.messages.append({"role": "assistant", "content": r.text})
        except Exception as e:
            # Hata olursa tam sebebini buraya yazacak
            st.error(f"⚠️ Hata: {str(e)}")

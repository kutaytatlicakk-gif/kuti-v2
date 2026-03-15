import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="KutiAİ VIP", page_icon="🤖")
st.title("🤖 KutiAİ VIP Asistan")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.error("🔑 API Key eksik!")
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
            r = model.generate_content(p)
            st.markdown(r.text)
            st.session_state.messages.append({"role": "assistant", "content": r.text})
        except:
            st.error("Bağlantı hatası!")

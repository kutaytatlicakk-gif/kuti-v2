import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="kutiAİ v11.0", page_icon="🤖")
st.title("🤖 kutiAİ v11.0")

# API Key Kontrolü
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # 404 hatasını geçmek için en garanti model ismi:
    model = genai.GenerativeModel("gemini-pro")
else:
    st.error("🔑 API Key bulunamadı! Secrets kısmına ekle.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if p := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)
    with st.chat_message("assistant"):
        try:
            # Yanıt alma
            response = model.generate_content(p)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"❌ Hata: {str(e)}")

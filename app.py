import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="kutiAİ v11.0", page_icon="🤖")

st.title("🤖 kutiAİ v11.0")

# API Key'i Secrets'tan çek
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Hangi modelin çalışacağını sistem otomatik denesin
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
    except:
        model = genai.GenerativeModel("gemini-pro")
else:
    st.error("🔑 API Key bulunamadı! Ayarlardan Secrets kısmına ekle.")
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
            # Yanıt almayı dene
            r = model.generate_content(p)
            st.markdown(r.text)
            st.session_state.messages.append({"role": "assistant", "content": r.text})
        except Exception as e:
            # Eğer yine hata verirse, model ismini değiştirip son bir kez daha dene
            try:
                model = genai.GenerativeModel("gemini-pro")
                r = model.generate_content(p)
                st.markdown(r.text)
                st.session_state.messages.append({"role": "assistant", "content": r.text})
            except:
                st.error(f"❌ Maalesef hala hata var: {str(e)}")

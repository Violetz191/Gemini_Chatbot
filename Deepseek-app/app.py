import streamlit as st
import google.generativeai as genai
import os

# Cấu hình Google Generative AI với API key từ biến môi trường
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY_NEW')
genai.configure(api_key=GOOGLE_API_KEY)

st.title("🐳 Chat Gemini 🐳")
st.subheader("🤖 Gemini Chatbot Prototype 🤖", divider="blue")

# Sidebar UI: cấu hình tham số cho LLM
st.sidebar.markdown("## Parameters")
st.sidebar.divider()
model = st.sidebar.radio("Choose LLM:", ("gemini-1.5-flash", "gemini-1.5-pro"))
temp = st.sidebar.slider("Temperature:", min_value=0.0, max_value=2.0, value=1.0, step=0.25)
top_p = st.sidebar.slider("Top P:", min_value=0.0, max_value=1.0, value=0.94, step=0.01)
max_tokens = st.sidebar.slider("Maximum Tokens:", min_value=100, max_value=5000, value=2000, step=100)

# Lưu lịch sử chat trong session_state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if prompt := st.chat_input("Enter your message:"):
    try:
        # Thêm prompt của người dùng vào lịch sử chat
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Hiển thị tin nhắn của người dùng
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Tạo placeholder để hiển thị phản hồi của Gemini
        with st.chat_message("assistant"):
            placeholder = st.empty()
        
        # Xây dựng ngữ cảnh hội thoại (thêm message hệ thống ban đầu)
        messages = [{"role": "system", "content": "You're a helpful assistant"}] + st.session_state.chat_history
        conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        
        # Cấu hình tham số tạo nội dung cho Gemini
        generation_config = {
            "temperature": temp,
            "top_p": top_p,
            "max_output_tokens": max_tokens,
            "response_mime_type": "text/plain",
        }
        
        # Tạo instance model và gọi API để tạo nội dung
        model_instance = genai.GenerativeModel(model_name=model, generation_config=generation_config)
        response = model_instance.generate_content([conversation_text])
        full_response = response.text
        
        # Hiển thị phản hồi từ Gemini
        placeholder.write(full_response)
        
        # Lưu lại phản hồi của assistant vào lịch sử chat
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})
        
    except Exception as e:
        st.error(f"Error: {e}")

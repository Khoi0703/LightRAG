import streamlit as st
import requests

# URL của FastAPI
API_URL = "http://localhost:8000/chatbot/"

# Hàm gọi API chatbot
def call_chatbot_api(user_input, mode="local"):
    payload = {"text": user_input, "mode": mode}
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        return response.json().get("response", "No response from chatbot.")
    else:
        return f"Error: {response.status_code} - {response.text}"

# Thiết lập giao diện Streamlit
st.set_page_config(page_title="Chatbot", layout="wide")

st.title("🤖 Chatbot với LightRAG")
st.markdown("Chào mừng bạn đến với chatbot. Hãy nhập câu hỏi của bạn bên dưới!")

# Tạo sidebar để chọn chế độ
mode = st.sidebar.selectbox(
    "Chọn chế độ",
    options=["local", "hybrid", "global", "naive"],
    help="Chế độ chat hoặc trả lời câu hỏi.",
)

# Lưu trữ lịch sử hội thoại
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "my_text" not in st.session_state:
    st.session_state.my_text = ""
def submit():
    st.session_state.my_text = st.session_state.user_input
    st.session_state.user_input = ""
st.text_area("Nhập tin nhắn của bạn:", key="user_input", height=100,on_change=submit)
user_input = st.session_state.my_text
if st.button("Gửi"):
    if user_input.strip():
        # Hiển thị câu hỏi của người dùng
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Gọi API chatbot
        bot_response = call_chatbot_api(user_input, mode=mode)

        # Hiển thị phản hồi của bot
        st.session_state.chat_history.append({"role": "bot", "content": bot_response})
        

    else:
        st.warning("Vui lòng nhập câu hỏi trước khi gửi!")


for message in st.session_state.chat_history:
    role = "👤" if message["role"] == "user" else "🤖"
    st.markdown(f"**{role}**: {message['content']}")

if st.button("Xóa lịch sử"):
    st.session_state.chat_history = []
    st.success("Đã xóa lịch sử hội thoại.")

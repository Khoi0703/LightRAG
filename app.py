import streamlit as st
import requests

API_URL = "http://localhost:8000/chatbot/"

st.set_page_config(page_title="Voz RAG Chatbot", layout="wide")
st.title("🤖 Voz Forum RAG Chatbot")
st.caption("Đặt câu hỏi về các cuộc thảo luận trên diễn đàn Voz.vn")

# Sidebar: chọn chế độ truy vấn
mode = st.sidebar.selectbox(
    "Chế độ truy vấn",
    options=["hybrid", "local", "global", "naive"],
    help=(
        "hybrid: Kết hợp vector + graph (khuyên dùng)\n"
        "local: Tìm kiếm cục bộ, câu hỏi cụ thể\n"
        "global: Tổng hợp toàn bộ đồ thị\n"
        "naive: Vector search thuần túy"
    ),
)

if st.sidebar.button("🗑️ Xóa lịch sử"):
    st.session_state.chat_history = []
    st.rerun()

# Khởi tạo lịch sử chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Hiển thị lịch sử hội thoại bằng st.chat_message
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Ô nhập câu hỏi
user_input = st.chat_input("Nhập câu hỏi của bạn...")

if user_input:
    # Hiển thị tin nhắn người dùng
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Gọi API và hiển thị phản hồi
    with st.chat_message("assistant"):
        with st.spinner("Đang xử lý..."):
            try:
                resp = requests.post(
                    API_URL,
                    json={"text": user_input, "mode": mode},
                    timeout=60,
                )
                if resp.status_code == 200:
                    bot_response = resp.json().get("response", "Không có phản hồi.")
                else:
                    bot_response = f"Lỗi {resp.status_code}: {resp.text}"
            except requests.exceptions.ConnectionError:
                bot_response = "❌ Không thể kết nối đến server. Hãy chắc chắn `server.py` đang chạy."
            except requests.exceptions.Timeout:
                bot_response = "⏱️ Server phản hồi quá lâu. Vui lòng thử lại."

        st.markdown(bot_response)

    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

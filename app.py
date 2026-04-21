import time
import streamlit as st
from agent.react_agent import ReactAgent

# 标题
st.title("智能冰箱客服")
st.divider()

# 初始化
if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 历史消息显示
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 用户输入
prompt = st.chat_input("请输入你的问题...")

if prompt:
    # 显示用户消息
    with st.chat_message("user"):
        st.write(prompt)

    st.session_state["messages"].append({
        "role": "user",
        "content": prompt
    })

    # 生成回复
    with st.chat_message("assistant"):
        with st.spinner("智能客服思考中..."):

            # ✅ 调用普通接口（稳定）
            result = st.session_state["agent"].execute(prompt)

            # ✅ 模拟流式输出
            full_response = ""
            placeholder = st.empty()

            for char in result:
                full_response += char
                placeholder.markdown(full_response)
                time.sleep(0.01)

    # 保存完整回复（关键修复点）
    st.session_state["messages"].append({
        "role": "assistant",
        "content": full_response
    })

    st.rerun()
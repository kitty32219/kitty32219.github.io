# streamlit_app.py
import os
import streamlit as st
from dotenv import load_dotenv
import aisuite as ai

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# 模型設定
provider = "groq"
model = "groq/compound"

def reply(system, prompt):
    client = ai.Client()
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(model=f"{provider}:{model}", messages=messages)
    return response.choices[0].message.content

# Streamlit 介面
st.title("🎯 DGIFood 商品貼文小幫手")

user_input = st.text_area("請輸入你的商品需求")
if st.button("生成貼文"):
    system_writer = "你是一位活潑、有趣的社群媒體幫手..."
    system_reviewer = "你是一位文案潤稿專家..."
    
    v1 = reply(system_writer, user_input)
    v2 = reply(system_reviewer, v1)
    v3 = reply(system_writer, f"這是原文：{v1}\n建議：{v2}\n請改寫")

    st.subheader("🌟 初稿")
    st.write(v1)
    st.subheader("🧐 修改建議")
    st.write(v2)
    st.subheader("✨ 最終推薦")
    st.write(v3)

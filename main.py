import streamlit as st
import requests
import os
import json

# -----------------------------
# 直接硬編碼金鑰（或改成 os.environ["GROQ_API_KEY"]）
# -----------------------------
API_KEY = ""
API_URL = "https://api.groq.com/openai/v1/chat/completions"

provider_model = "groq/compound"

# -----------------------------
# 定義對話函數
# -----------------------------
def reply(system, prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": provider_model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()  # 若出現錯誤會丟出例外
    data = response.json()
    
    # 解析回應內容
    return data["choices"][0]["message"]["content"]

# -----------------------------
# Streamlit 介面
# -----------------------------
st.title("🎯 DGIFood 商品貼文小幫手")

user_input = st.text_area("請輸入你的商品需求")
if st.button("生成貼文"):
    system_writer = "你很會查資料"
    system_reviewer = "你是一位文案潤稿專家..."
    
    try:
        prompt = f"繁體中文回答，商品需求：{user_input}\n商品資訊網址https://www.dgifood.com.tw/ 從中推薦適合的"
        v1 = reply(system_writer,  prompt)


        st.subheader("🌟 初稿")
        st.write(v1)
        st.subheader("🧐 修改建議")

    except Exception as e:
        st.error(f"生成貼文時出現錯誤: {e}")

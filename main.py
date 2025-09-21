import os
from dotenv import load_dotenv
import aisuite as ai

# 載入 .env 檔案中的 GROQ_API_KEY
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = api_key

provider_writer = "groq"
model_writer = "groq/compound"
provider_reviewer = "groq"
model_reviewer = "groq/compound"

system_writer = "你是一位活潑、有趣的社群媒體幫手，擅長幫我把日常分享變得更吸睛、第一人稱風格、有情緒、有 emoji，有時還帶點小幽默。請用台灣習慣的中文回應。"
system_reviewer = "你是一位文案潤稿專家，擅長讓貼文更口語、生活化、自然有趣，請針對以下貼文給出具體修改建議。請用台灣習慣的中文回應。"

def reply(system, prompt, provider="groq", model="groq/compound"):
    client = ai.Client()
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(model=f"{provider}:{model}", messages=messages)
    return response.choices[0].message.content

def reflect_post(prompt):
    first_version = reply(system_writer, prompt, provider_writer, model_writer)
    suggestion = reply(system_reviewer, first_version, provider_reviewer, model_reviewer)
    second_prompt = f"這是我剛剛寫的貼文：\n{first_version}\n\n這是修改建議：\n{suggestion}\n\n請根據這些建議，幫我改得更生活化、更自然。請用台灣習慣的中文, 並且只要輸出改好的文章就可以了。"
    second_version = reply(system_writer, second_prompt, provider_writer, model_reviewer)
    return first_version, suggestion, second_version

if __name__ == "__main__":
    user_prompt = input("請輸入你的商品需求：\n")
    v1, review, v2 = reflect_post(user_prompt)
    print("\n🌟 初稿：\n", v1)
    print("\n🧐 修改建議：\n", review)
    print("\n✨ 最終推薦：\n", v2)

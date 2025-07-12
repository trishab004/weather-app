from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

HF_API_KEY = os.environ.get("HF_API_KEY")  # Set this securely in Render

@app.route('/')
def home():
    return "🌤️ Trisha's Weather & Chatbot Backend Running!"

@app.route('/chat', methods=['POST'])
def chat_reply():
    data = request.get_json()
    user_message = data.get("message", "")

    print("📩 Prompt received:", user_message)

    url = "https://api-inference.huggingface.co/models/gpt2"


    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": user_message,
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.7,
            "top_p": 0.95
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    print("📡 HF API status:", response.status_code)
    print("🔁 Raw response:", response.text)

    if response.status_code == 200:
        result = response.json()
        reply = result[0].get("generated_text", "Sorry, no reply generated.")
        return jsonify({"reply": reply})
    else:
        print("❌ Hugging Face API call failed!")
        return jsonify({"reply": "Hugging Face API call failed. Check logs."}), 500

if __name__ == '__main__':
    app.run()

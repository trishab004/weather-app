from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

HF_API_KEY = os.environ.get("HF_API_KEY")  # Your Hugging Face API key in Render secrets

@app.route('/')
def home():
    return "🌤️ Trisha's Weather & Chatbot Backend Running on Hugging Face!"

@app.route('/gemini', methods=['POST'])
def gemini_reply():
    data = request.get_json()
    prompt = data.get("prompt", "")

    print("📩 Prompt received:", prompt)

    # Hugging Face text generation endpoint (example using a Hugging Face hosted model)
    url = "https://api-inference.huggingface.co/models/gpt2"  # or your chosen HF model

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        # Optional parameters to control output length, temperature, etc.
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.7,
            "top_p": 0.9
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    print("📡 Hugging Face API status:", response.status_code)
    print("🔁 Response raw:", response.text)

    if response.status_code == 200:
        result = response.json()
        # Hugging Face text generation usually returns a list with 'generated_text' key
        reply = result[0].get("generated_text", "Sorry, no reply generated.")
        return jsonify({"reply": reply})
    else:
        print("❌ Hugging Face API call failed!")
        return jsonify({"reply": "Hugging Face API call failed. Check logs."}), 500

if __name__ == '__main__':
    app.run()

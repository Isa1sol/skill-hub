from flask import request, jsonify
from app import app
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/ai-assist', methods=['POST'])
def ai_assist():
    user_input = request.json.get('query')
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful course assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return jsonify({"response": response['choices'][0]['message']['content']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

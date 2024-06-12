from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
OPENAI_API_KEY = 'IT MY API KEY'
CHATGPT_API_URL = 'https://api.openai.com/v1/chat/completions'

@app.route('/prompt', methods=['POST'])
def get_prompt():
    data = request.json
    if not data or 'prompt' not in data:
        return jsonify({'error': 'No prompt provided'}), 400

    prompt = data['prompt']

    response = requests.post(
        CHATGPT_API_URL,
        headers={
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'model': 'gpt-4',
            'messages': [{'role': 'user', 'content': prompt}]
        }
    )

    if response.status_code != 200:
        return jsonify({'error': 'Error from OpenAI API', 'details': response.json()}), 500

    chatgpt_response = response.json()
    reply = chatgpt_response['choices'][0]['message']['content']

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
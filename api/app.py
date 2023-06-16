from flask import Flask, request, render_template
import requests
import os
import json

app = Flask(__name__, template_folder=os.path.abspath('templates'))

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
chatgpt_api_url = "https://api.openai.com/v1/chat/completions"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']

        # Use OpenAI's API to get the response from ChatGPT
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_API_KEY}',
        }

        messages = [
            {"role": "user", "content": user_input}
        ]

        # Send the API request to ChatGPT
        chatgpt_response = requests.post(
            chatgpt_api_url,
            headers=headers,
            json={
                "messages": messages,
                "model": "gpt-3.5-turbo",
                "max_tokens": 2300,
                "temperature": 0.3
            }
        )

        # Handle the ChatGPT response and extract the adapted query
        if chatgpt_response.status_code == 200:
            chatgpt_result = chatgpt_response.json()
            chatgpt_result = chatgpt_result["choices"][0]["message"]["content"]
        else:
            print(chatgpt_response.status_code)
            print(chatgpt_response.content)

        return render_template('index.html', chatgpt_response=chatgpt_result)

    return render_template('index.html', chatgpt_response=None)

# Note: You don't need to have app.run() here as Vercel will handle running the application

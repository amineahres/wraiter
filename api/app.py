from flask import Flask, request, render_template
import requests
import os
import json

app = Flask(__name__, template_folder=os.path.abspath('templates'))

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']

        # Use OpenAI's API to get the response from ChatGPT
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_API_KEY}',
        }

        data = {
            'engine': 'davinci-codex',
            'prompt': user_input,
            'max_tokens': 100
        }

        response = requests.post('https://api.openai.com/v1/engines/davinci-codex/completions', headers=headers, data=json.dumps(data))
        chatgpt_response = response.json()["choices"][0]["message"]["content"]

        # Save data to Supabase (This part remains unchanged)
        # ... code to save data to Supabase ...

        return render_template('index.html', chatgpt_response=chatgpt_response)

    return render_template('index.html', chatgpt_response=None)

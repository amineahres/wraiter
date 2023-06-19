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

        # Retrieve all users inputs
        content_type = request.form['content_type']
        content_tone = request.form['content_tone']
        length = request.form['length']
        context = request.form['context']
        content = request.form['content']

        # Make sure that content is not null
        if content is None or len(content) < 10:
            chatgpt_result = "Please fill in the content with at least 10 characters."
            return render_template('index.html', chatgpt_response=chatgpt_result)
        else:
            # Create prompt
            prompt = ('Find between percent signs an input. from that input, please create a ' + content_type + 
            ' which has the following characteristics: \n' +
            '- Tone: ' + content_tone + ' \n' +
            '- Length: ' + length + ' \n' +
            'and take into account the following request: ' + context + ' \n' +
            '% \n' +
            content + 
            '\n%')
            
            print(prompt)
    
            # Use OpenAI's API to get the response from ChatGPT
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {OPENAI_API_KEY}',
            }
    
            messages = [
                {"role": "user", "content": prompt}
            ]
    
            # Send the API request to ChatGPT
            chatgpt_response = requests.post(
                chatgpt_api_url,
                headers=headers,
                json={
                    "messages": messages,
                    "model": "gpt-3.5-turbo",
                    "max_tokens": 600,
                    "temperature": 0.5
                }
            )
    
            # Handle the ChatGPT response and extract the adapted query
            chatgpt_result = None
    
            
            if chatgpt_response.status_code == 200:
                chatgpt_result = chatgpt_response.json()
                chatgpt_result = chatgpt_result["choices"][0]["message"]["content"]
            else:
                print(chatgpt_response.status_code)
                print(chatgpt_response.content)
                chatgpt_result = "Error: Failed to receive response from ChatGPT"
    
            return render_template('index.html', chatgpt_response=chatgpt_result)
    
    return render_template('index.html', chatgpt_response=None)

# Note: You don't need to have app.run() here as Vercel will handle running the application

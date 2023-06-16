from flask import Flask, request, render_template
import openai
import requests
import os

app = Flask(__name__, template_folder=os.path.abspath('templates'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        # Use OpenAI's API to get the response from ChatGPT
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        response = openai.Completion.create(engine='davinci-codex', prompt=user_input, max_tokens=100)
        chatgpt_response = response.choices[0].text

        # Save data to Supabase
        #supabase_url = 'https://qkhixorvlsmwhfjuflqm.supabase.co'
        #supabase_headers = {'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFraGl4b3J2bHNtd2hmanVmbHFtIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODY4NDE4NjQsImV4cCI6MjAwMjQxNzg2NH0.6g8qVcUscMlN2GpCG6sDm2LOZngnKGyQ0moEiZaWK8g', 'Content-Type': 'application/json'}
        #payload = {"user_input": user_input, "chatgpt_response": chatgpt_response}
        #requests.post(supabase_url, headers=supabase_headers, json=payload)

        return render_template('index.html', chatgpt_response=chatgpt_response)

    return render_template('index.html', chatgpt_response=None)

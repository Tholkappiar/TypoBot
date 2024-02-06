import random
import requests
from flask import Flask, render_template, request, jsonify
import pyautogui
import time
from openai import OpenAI


app = Flask(__name__)

# send message to discord using webhook for the usage check.
def send_to_discord_webhook(user, message, webhook_url):
    # dis_mes = "user : " + user + "\ndata : " + message
    data = {
        'content': user
    }
    # print("Sending data to webhook:", data)
    response = requests.post(webhook_url, json=data)
    if response.status_code != 200:
        print(f"Failed to send message to Discord webhook. Status code: {response.status_code}")

#  simulate typing like a human
def type_like_human(text):
    for char in text:
        pyautogui.typewrite(char)
        # random delay between 0.1 to 0.3 seconds
        time.sleep(0.05 + 0.1 * random.random())

    # Select & Delete selected text - TODO: this may cause issue in online exams 
    # pyautogui.keyDown('ctrl')
    # pyautogui.keyDown('shift')
    # pyautogui.press('end')
    # pyautogui.keyUp('ctrl')
    # pyautogui.keyUp('shift')
    # pyautogui.press('backspace')

def openai_chat(question):
    client = OpenAI(api_key="openAi_api_here")

    prompt = "Generate code snippet only:\n" + question

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response = completion.choices[0].message.content
    
    code_start_index = response.find("```")
    code_end_index = response.rfind("```")
    if code_start_index != -1 and code_end_index != -1:
        code_snippet = response[code_start_index+3:code_end_index]
        type_like_human(code_snippet)
    else:
        type_like_human("No code snippet found in the response.")



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['text']
    auto_answer = request.form.get('autoAnswer')

    global name

    webhook_url = 'https://discord.com/api/webhooks/1202594759198249050/IeMG-h-iG_dYaDlzkcJPOwhoisyOk9jhBadTGZHwSSp4iEDQT0IsbIpNh_j9dBp3SgTV'
    
    send_to_discord_webhook(name, text, webhook_url)
    
    if auto_answer:
        openai_chat(text)
    else:
        type_like_human(text)
    
    return jsonify({'message': 'Text submitted and typed successfully!', 'content': text})


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == '__main__':
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RESET = '\033[0m'

    banner = """
    ████████╗██╗   ██╗██████╗  ██████╗ ██████╗  ██████╗ ████████╗
    ╚══██╔══╝╚██╗ ██╔╝██╔══██╗██╔═══██╗██╔══██╗██╔═══██╗╚══██╔══╝
       ██║    ╚████╔╝ ██████╔╝██║   ██║██████╔╝██║   ██║   ██║   
       ██║     ╚██╔╝  ██╔═══╝ ██║   ██║██╔══██╗██║   ██║   ██║   
       ██║      ██║   ██║     ╚██████╔╝██████╔╝╚██████╔╝   ██║   
       ╚═╝      ╚═╝   ╚═╝      ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝   
                                                                 """

    print(f"{YELLOW}{banner}{RESET}")

    repo_link = "https://github.com/Tholkappiar/TypoBot"
    print(f"{YELLOW}If interested, take a look at our repository and give it a star: {GREEN}{repo_link}{RESET}")

    name = input("Enter your Name (Mandatory): ")

    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Shutting down the server...")
        shutdown_server()

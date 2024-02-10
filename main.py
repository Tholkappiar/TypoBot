import random
import requests
from flask import Flask, render_template, request, jsonify
import time
from openai import OpenAI
from pynput.keyboard import Controller

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
    keyboard = Controller()
    for char in text:
        # using pynput KeyBoard package instead of pyautogui due to the issues in the char type errors.
        # i.e : "<" identified as ">"
        # pyautogui.typewrite(char, interval=0.01)
        keyboard.type(char)
        # random delay between 0.1 to 0.3 seconds
        time.sleep(random.uniform(0.1, 0.3))

    # Select & Delete selected text - TODO: this may cause unexpected issues in online exams 
    # pyautogui.keyDown('ctrl')
    # pyautogui.keyDown('shift')
    # pyautogui.press('end')
    # pyautogui.keyUp('ctrl')
    # pyautogui.keyUp('shift')
    # pyautogui.press('backspace')

def openai_chat(question):
    client = OpenAI(api_key="api-here")

    prompt = """Please provide a concise code snippet block in Python without any comments or 
    additional snippets, including all necessary imports, to address the following question: \n""" + question

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response = completion.choices[0].message.content
    code_snippet = extract_code_snippet(response)

    type_like_human(code_snippet)

def extract_code_snippet(response):
    # Extract the code snippets by leaving explanations and other comments.
    start_index = response.find("```")
    end_index = response.rfind("```")
    code_snippet = response[start_index + 3:end_index]
    # Remove whitespace and indentation
    lines = code_snippet.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    min_indent = min(len(line) - len(line.lstrip()) for line in non_empty_lines)
    processed_lines = [line[min_indent:] for line in non_empty_lines]

    # Reconstruct code snippet
    code_snippet = '\n'.join(processed_lines)
    return code_snippet



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

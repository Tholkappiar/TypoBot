from flask import Flask, render_template, request, jsonify
import random
import time
import requests
from pynput.keyboard import Controller

app = Flask(__name__)

def get_code_from_server(name,question):
    url = 'http://127.0.0.1:5000/get_code'
    payload = {'question': question,'name': name}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            code_snippet = data.get('code')
            type_like_human(code_snippet)
        else:
            type_like_human(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        type_like_human(f"Error occurred: {e}")

#  simulate typing like a human
def type_like_human(text):
    keyboard = Controller()
    for char in text:
        keyboard.type(char)
        time.sleep(random.uniform(0.1, 0.3))
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['text']
    auto_answer = request.form.get('autoAnswer')
    if auto_answer:
        get_code_from_server(name,text)
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
        app.run(host='0.0.0.0', port=5005)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Shutting down the server...")
        shutdown_server()
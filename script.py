import random
import os
from flask import Flask, render_template, request, jsonify
import pyautogui
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['text']
    type_like_human(text)
    return jsonify({'message': 'Text submitted and typed successfully!'})

def type_like_human(text):
    for char in text:
        pyautogui.typewrite(char)
        # random delay between 0.1 to 0.3 seconds
        time.sleep(0.05 + 0.1 * random.random())
        # time.sleep(0.1 + 0.2 * random.random())

    # Select & Delete selected text - TODO: this may cause issue in online exams 
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('shift')
    pyautogui.press('end')
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('shift')

    pyautogui.press('backspace')

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
    # ANSI escape codes for professional colors
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RESET = '\033[0m'

     # Banner
    banner = """
    ████████╗██╗   ██╗██████╗  ██████╗ ██████╗  ██████╗ ████████╗
    ╚══██╔══╝╚██╗ ██╔╝██╔══██╗██╔═══██╗██╔══██╗██╔═══██╗╚══██╔══╝
       ██║    ╚████╔╝ ██████╔╝██║   ██║██████╔╝██║   ██║   ██║   
       ██║     ╚██╔╝  ██╔═══╝ ██║   ██║██╔══██╗██║   ██║   ██║   
       ██║      ██║   ██║     ╚██████╔╝██████╔╝╚██████╔╝   ██║   
       ╚═╝      ╚═╝   ╚═╝      ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝   
                                                                 """

    # Print banner
    print(f"{YELLOW}{banner}{RESET}")

    # Repo link
    repo_link = "https://github.com/Tholkappiar"

    # Prompt the user to check out a repo and give it a star
    print(f"{YELLOW}If interested, take a look at our repository and give it a star: {GREEN}{repo_link}{RESET}")
    
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Shutting down the server...")
        shutdown_server()

import random
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

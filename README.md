# TypoBot

## Introduction
TypoBot is a Flask web application that simulates typing, like a human, by sending text from the device within the same network. It includes a Python script for simulating human-like typing behavior and an HTML form for submitting text.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/thols/TypoBot.git

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
## Usage
1. Run the Flask application:
    ```bash
    python script.py
2. Open a web browser and navigate to http://localhost:5000 to access it on the same device. Alternatively, use `ip:5000`, which will be shown in the script, to access the webpage on a different device within the same network.
3. Enter text in the provided textarea and click "Submit" to simulate typing.
4. To exit the script, always use `Ctrl + C`. This stops the script and kills the server. If any other interruptions occur or windows are closed unexpectedly, stop the process running in the background with port number 5000, or change the port number using any text editor.

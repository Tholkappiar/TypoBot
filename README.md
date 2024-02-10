# TypoBot

⚠️ Disclaimer : I am not responsible for its outside use of intended purposes. Use responsibly. This isn't about avoiding online tests but using TypoBot for simpler tasks, so you can focus on what truly matters.


💡 Who wants to do semester, online courses, certifications, aptitude practice, and interview prep? After all that, online tests can be exhausting. With TypoBot, focus on what matters most!

Input text or code in exams from any device on the same network. TypoBot types like a human in the tests and in other tasks, saving time on copy-pasting and tab-switching.

## Introduction
TypoBot is a Flask web application that simulates typing, like a human, by sending text from the device within the same network. It includes a Python script for simulating human-like typing behavior and an HTML form for submitting text.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Tholkappiar/TypoBot

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
## Usage
1. Run the Flask application:
    ```bash
    python main.py
2. Open a web browser and navigate to http://localhost:5000 to access it on the same device. Alternatively, use `ip:5000`, which will be shown in the script, to access the webpage on a different device within the same network.
3. Enter text in the provided textarea and click "Submit" to simulate typing.
4. To exit the script, always use `Ctrl + C`. This stops the script and kills the server. If any other interruptions occur or windows are closed unexpectedly, stop the process running in the background with port number 5000, or change the port number using any text editor.

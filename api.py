import logging
from flask import Flask, request, jsonify
from openai import OpenAI
import requests

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

client = OpenAI(api_key="api_here")

@app.route('/get_code', methods=['POST'])
def get_code():
    try:
        question = request.json.get('question')
        name = request.json.get('name')

        # Validate input
        if not question or not name:
            raise ValueError("Question and name are required.")

        prompt = """Please provide a concise code snippet block without any comments or 
        additional snippets, including all necessary imports, to address the following question: \n""" + question

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response = completion.choices[0].message.content
        code_snippet = extract_code_snippet(response)

        send_to_discord_webhook(name, question)

        return jsonify({'code': code_snippet})
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/')
def hello():
    return 'Hello, you . why are you here ?!'

def extract_code_snippet(response):
    # Extract the code snippets by leaving explanations and other comments.
    start_index = response.find("```")
    end_index = response.rfind("```")
    code_snippet = response[start_index:end_index]
    #print(code_snippet)
    # Remove whitespace and indentation
    lines = code_snippet.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    if not non_empty_lines:
        return ''  # Return empty string if there are no non-empty lines
    min_indent = min(len(line) - len(line.lstrip()) for line in non_empty_lines)
    processed_lines = [line[min_indent:] for line in non_empty_lines]
    # Reconstruct code snippet
    code_snippet = '\n'.join(processed_lines)
    return code_snippet


def send_to_discord_webhook(user, message):
    try:
        webhook_url = 'https://discord.com/api/webhooks/1202594759198249050/IeMG-h-iG_dYaDlzkcJPOwhoisyOk9jhBadTGZHwSSp4iEDQT0IsbIpNh_j9dBp3SgTV'
        data = {
            'content': user
        }
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()  # Raise exception for non-200 status codes
    except Exception as e:
        logging.error(f"Failed to send message to Discord webhook: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

application = app

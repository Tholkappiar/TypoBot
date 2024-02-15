import requests

def get_code_from_server(name, question):
    url = 'http://127.0.0.1:5000/get_code'
    payload = {'question': question, 'name': name}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            code_snippet = data.get('code')
            print("Code Snippet:")
            print(code_snippet)
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error occurred: {e}")

# Example usage:
name = "your_name"
question = "give the python program for hello world?"
get_code_from_server(name, question)

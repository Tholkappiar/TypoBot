from openai import OpenAI

client = OpenAI(api_key="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")

# Define the user prompt message
prompt = "Hello!"

# Create a chatbot using ChatCompletion.create() function
msg = input("Enter the msg to send to openai : ")
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": msg},
        {"role": "user", "content": prompt}
    ]
)

# Extract and print only the code snippet
response = completion.choices[0].message.content
code_start_index = response.find("```")
code_end_index = response.rfind("```")
if code_start_index != -1 and code_end_index != -1:
    code_snippet = response[code_start_index:code_end_index+3]
    print(code_snippet)
else:
    print("No code snippet found in the response.")


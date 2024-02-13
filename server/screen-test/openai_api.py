from openai import OpenAI



def answer(question):
    
    client = OpenAI(api_key="api_here")

    prompt = """This is the competitive programming question but other unwanted text also included so ignore
            that text which are not usefull for the context question and give the code snippet for this question : """
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt + question}
        ]
    )
    response = completion.choices[0].message.content
    code_start_index = response.find("```")
    code_end_index = response.rfind("```")
    if code_start_index != -1 and code_end_index != -1:
        code_snippet = response[code_start_index:code_end_index+3]
        print(code_snippet)
    else:
        print("No code snippet found in the response.")
from openai import OpenAI


def chatgpt4(instruction, question, re):
    messages = [
        {"role": "system", "content": instruction},
        {"role": "user", "content": question}
    ]
    client = OpenAI(
        base_url="https://api-key.info/v1/",
        api_key="sk-bfjGXNIjsGLzzBH83f6d430a17C3475186C05e7b4a5665Cf"
    )
    completion = client.chat.completions.create(
      model="gpt-4",
      messages=messages
    )
    return completion.choices[0].message.content

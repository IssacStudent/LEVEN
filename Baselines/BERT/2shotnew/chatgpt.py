from openai import OpenAI


def chatgpt(instruction, question, re):
    messages = [
        {"role": "system", "content": instruction},
        {"role": "user", "content": question}
    ]
    client = OpenAI(
        base_url="https://api.chatgptid.net/v1",
        api_key="sk-tP58U4K1gSVBMeYL3e0a7a03FbBe44B0B80bDd919505FcB7"
    )
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=messages
    )
    return completion.choices[0].message.content
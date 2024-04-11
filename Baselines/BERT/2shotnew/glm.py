from zhipuai import ZhipuAI

client = ZhipuAI(api_key="abe10659f2d516bd0c3db5fcefcfa308.9cY2LSN2Zmi8wuZi")  # 填写您自己的APIKey


def glm4(instruction, question, re):
    try:
        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": question}
            ],
        )
    except Exception as e:
        print("error:" + question)
        return None
    return response.choices[0].message.content

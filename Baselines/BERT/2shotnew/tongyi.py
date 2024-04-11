import random
from http import HTTPStatus
import dashscope
import os


def tongyi(instruction, question, re):
    messages = [{'role': 'system', 'content': instruction},
                {'role': 'user', 'content': question}]
    dashscope.api_key = 'sk-563fd3dd81dd4f858c75a9622468a29a'
    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_max,
        messages=messages,
        # set the random seed, optional, default to 1234 if not set
        seed=random.randint(1, 10000),
        # set the result to be "message" format.
        result_format='message',
    )
    if response.status_code == HTTPStatus.OK:
        return extract_content_from_response(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
        if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            if re:
                return None
            else:
                return "resend"
        return None


def extract_content_from_response(response):
    try:
        # Navigate through the response to get to the 'content'
        content = response["output"]["choices"][0]["message"]["content"]
        return content
    except (KeyError, IndexError) as e:
        print(f"Error extracting content from response: {e}")
        return None

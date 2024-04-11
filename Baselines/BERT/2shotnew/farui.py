import traceback

import requests
import hashlib
import time
import random
import json

# Replace these with your actual credentials
appId = "g09a3z1m"
appKey = "j90p63zb5ch2k4a1"
secret = "23wu0v6v59anpxi3"
# API endpoint
url = "https://tyfarui.biz.aliyun.com/open/legalMind/detailTalkAsyn.json"
ins = "下面是一句法律文本，请判断这句文本触发了哪个事件，注意每句话只有一个事件。事件包括：支付/给付,欺骗,搜查/扣押,要求/请求,同意/接受,拘捕,买入,获利,鉴定,卖出,租用/借用,受伤,帮助/救助,供述,伪造,联络,赔偿,卖淫,归还/偿还,制造,伤害人身,提供,组织/安排,通知/提醒,威胁/强迫,签订合同/订立协议,投案,受损,共谋,运输/运送,退赃,谅解,逃匿,冒充,贿赂,交通事故,约定,吸毒,盗窃财物,介绍/引荐,指使/教唆,持械/持枪,猥亵,报警/报案,嫖娼,死亡,阻止/妨碍,分赃,违章驾驶,赌博,毁坏财物,销赃,明知,抢夺财物,建议,雇佣,贩卖毒品,买卖,拒绝/抗拒,变造,侵占财物,邀请/招揽,饮酒,肢体冲突,纠集,放弃/停止,冲突,放火,挪用财物,拘束/拘禁,私藏/藏匿,强奸,言语冲突,入室/入户,遗弃,集资,事故,暴力,火灾事故,爆炸事故,绑架,出租/出借,邮寄,举报,抢劫财物,开设赌场,跟踪,敲诈勒索,放贷,拐骗,放纵,散布,走私,言语辱骂,杀害,自杀,租/借,遗失,昏迷,泄露信息,投毒,中毒,自然灾害,洪涝,山体滑坡,挑衅/挑拨,被困,干旱一共108种，你的答案必须完全来自于上面的108种事件类型，不能自己创造新的事件类型。请直接给出触发的事件，例如“支付/给付”，请你严格按照这个格式回答，不能在答案前面加上任何内容，如“事件：”或“触发的事件：”等等。下面是几个例子\n句子：经鉴定，被害人李某某的损伤程度属轻微伤\n鉴定\n句子：张士兵为了请刘玉宏对其违规建房问题给予关照，在其邻居小黄开的首饰店里以2500元的价格购买一块金镶玉送给刘玉宏\n要求/请求\n接下来是你要判断的句子: \n"


def farui(instruction, question, bizId):

    try:
        # Generate timestamp and random string
        timestamp = str(int(time.time() * 1000))
        random_str = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16))


        # Calculate signature
        signature_raw = appId + appKey + timestamp + random_str + secret
        signature = hashlib.md5(signature_raw.encode('utf-8')).hexdigest()

        # Request data
        data = {
            "input": {
                "prompt": ins + question,
            },
            "appId": appId,
            "appKey": appKey,
            "timestamp": timestamp,
            "random": random_str,
            "signature": signature,
            "bizId": bizId
        }

        # Send request
        headers = {'Content-Type': 'application/json;charset=UTF-8'}
        # 循环判断返回的状态，直到返回的状态为200且finish_status为true
        cnt = 0
        while True:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            if response.json()['code'] == 200:
                returned_data = response.json()['data']['output']
                # 不断轮询直到returnedData的finish_status为true
                while not returned_data['finish_status']:
                    time.sleep(1)
                    response = requests.post(url, headers=headers, data=json.dumps(data))
                    returned_data = response.json()['data']['output']

                returned_text = returned_data['text']
                return returned_text
            elif response.json()['code'] == 1509:
                print('触发限流')
                cnt += 1
                if cnt > 10:
                    return None
                time.sleep(20)
            else:
                return None
    except Exception as e:
        # 打印详细的错误信息
        print(e.args)
        print("=====")
        print(traceback.format_exc())

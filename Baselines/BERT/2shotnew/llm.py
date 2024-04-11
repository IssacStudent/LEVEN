import json
import random

from tqdm import tqdm


def construct_k_shot_dataset(k, train_file, valid_file, n):
    # 加载训练集和测试集数据
    with open(train_file, 'r', encoding='utf-8') as f:
        train_data = [json.loads(line) for line in f.readlines()]

    with open(valid_file, 'r', encoding='utf-8') as f:
        valid_data = [json.loads(line) for line in f.readlines()]

    # 随机选择K个示例作为提示信息
    k_samples = random.sample(train_data, k)

    # 构建K-shot提示信息
    instruction_base = """下面是一句法律文本，请判断这句文本触发了哪个事件，事件包括：\n"""
    event_types = [
        "支付/给付", "欺骗", "搜查/扣押", "要求/请求", "同意/接受", "拘捕", "买入", "获利", "鉴定", "卖出",
        "租用/借用", "受伤", "帮助/救助", "供述", "伪造", "联络", "赔偿", "卖淫", "归还/偿还", "制造",
        "伤害人身", "提供", "组织/安排", "通知/提醒", "威胁/强迫", "签订合同/订立协议", "投案", "受损", "共谋",
        "运输/运送",
        "退赃", "谅解", "逃匿", "冒充", "贿赂", "交通事故", "约定", "吸毒", "盗窃财物", "介绍/引荐",
        "指使/教唆", "持械/持枪", "猥亵", "报警/报案", "嫖娼", "死亡", "阻止/妨碍", "分赃", "违章驾驶", "赌博",
        "毁坏财物", "销赃", "明知", "抢夺财物", "建议", "雇佣", "贩卖毒品", "买卖", "拒绝/抗拒", "变造",
        "侵占财物", "邀请/招揽", "饮酒", "肢体冲突", "纠集", "放弃/停止", "冲突", "放火", "挪用财物", "拘束/拘禁",
        "私藏/藏匿", "强奸", "言语冲突", "入室/入户", "遗弃", "集资", "事故", "暴力", "火灾事故", "爆炸事故",
        "绑架", "出租/出借", "邮寄", "举报", "抢劫财物", "开设赌场", "跟踪", "敲诈勒索", "放贷", "拐骗",
        "放纵", "散布", "走私", "言语辱骂", "杀害", "自杀", "租/借", "遗失", "昏迷", "泄露信息",
        "投毒", "中毒", "自然灾害", "洪涝", "山体滑坡", "挑衅/挑拨", "被困", "干旱"
    ]
    instruction_base += ",".join(event_types) + ""
    instruction_base += "\n一共108种。请直接给出触发的事件，例如“支付/给付”。请你严格按照这个格式回答。下面是几个例子\n"

    # 添加K个示例到指令中
    for sample in k_samples:
        for event in sample["events"]:
            event_type = event["type"]
            sent_id = event["mention"][0]["sent_id"]
            sentence = sample["content"][sent_id]["sentence"]
            instruction_base += f"句子：{sentence}\n{event_type}\n"
    instruction_base += "接下来是你要判断的句子: \n"

    # 构建n条数据
    output_data = []
    for i in tqdm(range(n)):
        valid_sample = random.choice(valid_data)
        for event in valid_sample["events"]:
            event_type = event["type"]
            sent_id = event["mention"][0]["sent_id"]
            question_sentence = valid_sample["content"][sent_id]["sentence"]
            output_data.append({
                "instruction": instruction_base,
                "question": f"{question_sentence}",
                "answer": event_type
            })

    # 保存到JSON文件
    with open(str(k) + "_shot_dataset_5.json", 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)


# 示例调用函数
construct_k_shot_dataset(2, "train.jsonl", "valid.jsonl", 5)


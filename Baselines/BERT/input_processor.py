import jieba


class InputExample(object):
    """
        A single training/test example for token classification.
        one single sequence of tokens is an example in LEVEN task.
    """

    def __init__(self, sentence, words, labels):
        self.sentence = sentence
        self.words = words
        self.labels = labels


class InputFeatures(object):
    """A single set of features of data."""

    def __init__(self, input_ids, input_mask, segment_ids, label_ids):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        self.label_ids = label_ids


def split_chinese_sentences(text):
    # 定义中文分句标点
    punctuation_marks = set(['。', '！', '？', '；'])
    sentences = []
    start = 0  # 句子开始位置

    # 遍历文本进行分句
    for i, char in enumerate(text):
        if char in punctuation_marks:
            # 捕获句子并去除末尾的分句标点
            sentence = text[start:i].strip()
            if sentence:
                sentences.append(sentence)
            start = i + 1

    # 捕获最后一个句子（如果存在且不以分句标点结束的话）
    if start < len(text):
        sentence = text[start:].strip()
        sentences.append(sentence)

    return sentences


def construct_examples(sentences):
    examples = []
    for sentence in sentences:
        words = list(jieba.cut(sentence))
        labels = ['O'] * len(words)
        examples.append(InputExample(
                sentence=sentence,
                words=words,
                labels=labels
            )
        )
    return examples


def convert_examples_to_features(examples,
                                 label_list,
                                 max_seq_length,
                                 tokenizer,
                                 cls_token_at_end=False,
                                 cls_token="[CLS]",
                                 cls_token_segment_id=0,
                                 sep_token="[SEP]",
                                 sep_token_extra=False,
                                 pad_on_left=False,
                                 pad_token=0,
                                 pad_token_segment_id=0,
                                 pad_token_label_id=-100,
                                 sequence_a_segment_id=0,
                                 mask_padding_with_zero=True):
    label_map = {label: i for i, label in enumerate(label_list)}

    # my logic in crf_padding requires this check. I create mask for crf by labels==pad_token_label_id to not include it
    # in loss and decoding
    assert pad_token_label_id not in label_map.values()

    features = []
    for ex_index, example in enumerate(examples):

        tokens = []
        label_ids = []
        for word, label in zip(example.words, example.labels):
            word_tokens = tokenizer.tokenize(word)
            if len(word_tokens) == 0:
                word_tokens = ['<UNK>']
            tokens.extend(word_tokens)
            # Use the real label id for the first token of the word, and padding ids for the remaining tokens
            label_ids.extend([label_map[label]] + [pad_token_label_id] * (len(word_tokens) - 1))

        # Account for [CLS] and [SEP] with "- 2" and with "- 3" for RoBERTa.
        special_tokens_count = 3 if sep_token_extra else 2
        if len(tokens) > max_seq_length - special_tokens_count:
            tokens = tokens[:(max_seq_length - special_tokens_count)]
            label_ids = label_ids[:(max_seq_length - special_tokens_count)]

        tokens += [sep_token]
        label_ids += [pad_token_label_id]  # [label_map["X"]]

        if sep_token_extra:
            # roberta uses an extra separator b/w pairs of sentences
            tokens += [sep_token]
            label_ids += [pad_token_label_id]
        segment_ids = [sequence_a_segment_id] * len(tokens)

        if cls_token_at_end:
            tokens += [cls_token]
            label_ids += [pad_token_label_id]
            segment_ids += [cls_token_segment_id]
        else:
            tokens = [cls_token] + tokens
            label_ids = [pad_token_label_id] + label_ids
            segment_ids = [cls_token_segment_id] + segment_ids

        # 转化为input_ids
        input_ids = tokenizer.convert_tokens_to_ids(tokens)

        # The mask has 1 for real tokens and 0 for padding tokens. Only real
        # tokens are attended to.
        input_mask = [1 if mask_padding_with_zero else 0] * len(input_ids)

        # Zero-pad up to the sequence length.
        padding_length = max_seq_length - len(input_ids)
        if pad_on_left:
            input_ids = ([pad_token] * padding_length) + input_ids
            input_mask = ([0 if mask_padding_with_zero else 1] * padding_length) + input_mask
            segment_ids = ([pad_token_segment_id] * padding_length) + segment_ids
            label_ids = ([pad_token_label_id] * padding_length) + label_ids

        else:
            input_ids += ([pad_token] * padding_length)
            input_mask += ([0 if mask_padding_with_zero else 1] * padding_length)
            segment_ids += ([pad_token_segment_id] * padding_length)
            label_ids += ([pad_token_label_id] * padding_length)

        assert len(input_ids) == max_seq_length
        assert len(input_mask) == max_seq_length
        assert len(segment_ids) == max_seq_length
        assert len(label_ids) == max_seq_length

        features.append(
            InputFeatures(input_ids=input_ids,
                          input_mask=input_mask,
                          segment_ids=segment_ids,
                          label_ids=label_ids))
    return features


def process_input_examples(input_examples):
    results = []

    for example in input_examples:
        events = []  # 存储触发词和对应的事件类型及偏移位置
        sentence = example.sentence
        words = example.words
        labels = example.labels

        # 确保words和labels的长度相同
        assert len(words) == len(labels), "Words and labels must have the same length."

        # 初始化偏移位置
        offset = 0
        for i, (word, label) in enumerate(zip(words, labels)):
            if label != 'O':  # 如果标签不是'O'，则为触发词
                event_type = label[2:]  # 去掉前面的'B-'或'I-'
                start = sentence.find(word, offset)  # 从当前偏移位置开始查找单词
                end = start + len(word)
                events.append({
                    'type': event_type,
                    'trigger': word,
                    'start': start,
                    'end': end
                })

                # 更新下一个单词的起始偏移位置
                offset = start + len(word)

        result = {
            'sentence': example.sentence,
            'events': events
        }
        results.append(result)

    return results

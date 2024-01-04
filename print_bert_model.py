from transformers import (
    BertForTokenClassification,
    BertTokenizer,
    BertConfig,
    BertPreTrainedModel,
    BertForMaskedLM,
    BertForMultipleChoice,
    BertForQuestionAnswering,
    BertForSequenceClassification,
    BertForNextSentencePrediction,
    BertForPreTraining,
    BertModel
)

from Baselines.BERT.utils_leven import get_labels

MODEL_CLASSES = {
    1: (BertConfig, BertPreTrainedModel, BertTokenizer),
    2: (BertConfig, BertForMaskedLM, BertTokenizer),
    3: (BertConfig, BertForMultipleChoice, BertTokenizer),
    4: (BertConfig, BertForQuestionAnswering, BertTokenizer),
    5: (BertConfig, BertForSequenceClassification, BertTokenizer),
    6: (BertConfig, BertForNextSentencePrediction, BertTokenizer),
    7: (BertConfig, BertForPreTraining, BertTokenizer),
    8: (BertConfig, BertModel, BertTokenizer),
}

modelList = [
    BertPreTrainedModel,
    BertForMaskedLM,
    BertForMultipleChoice,
    BertForQuestionAnswering,
    BertForSequenceClassification,
    BertForNextSentencePrediction,
    BertForPreTraining,
    BertModel
]

labels = get_labels()
num_labels = len(labels)

for i in range(9):
    if i == 0:
        continue
    config_class, model_class, tokenizer_class = MODEL_CLASSES[i]
    config = config_class.from_pretrained("bert-base-chinese",
                                          num_labels=num_labels,
                                          cache_dir=None)

    ner_model = model_class.from_pretrained(
        "bert-base-chinese",
        from_tf=bool(".ckpt" in "bert-base-chinese"),
        config=config,
        cache_dir=None,
    )
    print(ner_model, file=open("./model.txt", 'a+', encoding='utf-8'))
    print("-----------------------------------------------------------------------",
          file=open("./model.txt", 'a+', encoding='utf-8'))

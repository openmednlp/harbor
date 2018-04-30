from bedrock import common
import bedrock
import json
from configparser import ConfigParser
import dill

config = ConfigParser()
config.read('config.ini')


def predict(text):
    with open(config['DEFAULT']['sentence_tokenizer'], 'rb') as f:
        sentence_tokenizer = dill.load(f)

    with open(config['DEFAULT']['preprocessor'], 'rb') as f:
        preprocessor = dill.load(f)

    vectorizer = common.load_pickle(config['DEFAULT']['vectorizer'])

    model = common.load_pickle(config['DEFAULT']['model'])

    result = dict()
    result['result'] = []

    # Do text split with another vectorizer
    sentences = sentence_tokenizer(text)
    processed_sentences = [preprocessor(s) for s in sentences][0]
    sentences = sentences[0]  # Don't ask TODO: Fix it

    vectors = vectorizer.transform(processed_sentences)

    labels = [int(model.predict(v)) for v in vectors]

    text_dict = dict()
    text_dict['segments'] = [
        {
            'segment': sentence,
            'processed_segment': processed_sentence,
            'label': label,
            'label_text': label2text(label)
        }
        for sentence, processed_sentence, label
        in zip(sentences, processed_sentences, labels)
    ]

    # max in order of 5, 4, 2, 1, 3, 0
    score_weight = [0, 2, 3, 1, 4, 5]
    text_dict['overall_label'] = max(
        labels,
        key=lambda x: score_weight[x]
    )

    text_dict['overall_label_text'] = label2text(text_dict['overall_label'])

    result['result'].append(text_dict)

    return json.dumps(result)


def label2text(label):
    label_dict = {
        0: 'Void',
        1: 'Negative',
        2: 'Somewhat Negative',
        3: 'Ambiguous',
        4: 'Somewhat Positive',
        5: 'Positive'
    }
    return label_dict[label]


if __name__ == '__main__':
    print('Running playground, not meant for production.')

    json_text = predict(
        'Es gibt ein gorsses Tumor. Oder kein Tumor. Was ist Tumor.'
    )

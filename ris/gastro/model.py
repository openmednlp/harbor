from bedrock import common
import bedrock
import json
from configparser import ConfigParser
import dill


def predict(text, config):
    with open(config['IMPRESSION_EXTRACTOR'], 'rb') as f:
        impression_extractor = dill.load(f)

    with open(config['SENTENCE_TOKENIZER'], 'rb') as f:
        sentence_tokenizer = dill.load(f)

    with open(config['PREPROCESSOR'], 'rb') as f:
        preprocessor = dill.load(f)

    vectorizer = common.load_pickle(config['VECTORIZER'])
    model = common.load_pickle(config['MODEL'])

    result = dict()
    result['result'] = None

    impression = impression_extractor(text)
    if not impression:
        return json.dumps({})
    sentences = sentence_tokenizer(impression)
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

    text_dict['report'] = text

    text_dict['impression'] = impression

    # max in order of 5, 4, 2, 1, 3, 0
    score_weight = [0, 2, 3, 1, 4, 5]
    text_dict['overall_label'] = max(
        labels,
        key=lambda x: score_weight[x]
    )
    text_dict['overall_label_text'] = label2text(text_dict['overall_label'])
    result['result'] = text_dict

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
        '''
        Unknown Header
        
        Something before in another header.
        
        Beurteilung
        
        Es gibt ein gorsses Tumor. Oder kein Tumor. Was ist Tumor.
        Und jetzt...nichts.
        
        Ciao!
        ''',
        None
    )
    print(json_text)
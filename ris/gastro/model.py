from bedrock import common
import json


#path = common.get_latest_file('/home/giga')
_inputs = None #make default if loaded


def get_inputs():
    return None, None, None

import random
def classify(x):
    return random.randint(0, 5)

def predict(texts):
    if type(texts) == str:
        texts = [texts]

    # TODO: make location
    inputs = get_inputs()

    # classifier = common.load_pickle(inputs['classifier'])
    # sentence_spliter = common.load_pickle(inputs['senttence_splitter'])
    # process_pipeline = common.load_pickle(inputs['process_pipeline'])

    result = dict()
    result['texts'] = []

    for text in texts:
        # Do text split with another vectorizer
        segments = text.split('.')

        text_labels = [classify(segment) for segment in segments]

        text_dict = dict()
        text_dict['segments'] = [
            {
                'bedrock': segment,
                'label': label,
                'label_text': label2text(label)
            }
            for segment, label in zip(segments, text_labels)
        ]

        # max in order of 5, 4, 2, 1, 3, 0
        score_weight = [0, 2, 3, 1, 4, 5]
        text_dict['overall_label'] = max(
            text_labels,
            key=lambda x: score_weight[x]
        )

        text_dict['overall_label_text'] = label2text(text_dict['overall_label'])

        result['texts'].append(text_dict)

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

    jtext = predict(
        ['abc es gibt ein gorsses tumor. oder kein tumor. was ist tumor.',
         '123 123 aaa vvv kein tumor. etwas neues.']
    )
    print(jtext)


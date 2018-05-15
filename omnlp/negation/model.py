import dill


def predict(text, config):
    with open(config['LABELER'], 'rb') as f:
        labeler = dill.load(f)

    df = labeler(text)

    return df.to_json()

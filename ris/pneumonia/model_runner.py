import dill


def predict(text, config):
    with open(
            '/Users/giga/Dev/USB/workshop/shipyard/ris/pneumonia/output/model.dill',
            'rb') as f:
        labeler = dill.load(f)
        
    result = labeler(text)
    
    return result

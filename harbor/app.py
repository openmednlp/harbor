from ris.gastro.model import predict as gastro_predict
from ris.pneumonia.model_runner import predict as pneumonia_predict


from flask import request, Flask
import json

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('harbor.default_config')
app.config.from_pyfile('config.cfg', silent=False)


@app.route('/')
def root():
    return (
        json.dumps({'success': True}),
        200,
        {'ContentType': 'application/json'}
    )


@app.route('/predict', methods=['POST'])
def predict():
    input_text = request.form['input_text']
    response = gastro_predict(input_text, app.config)
    return response


@app.route('/predict/pneumonia', methods=['POST'])
def pneumonia():
    # read -s text
    # curl -X POST -F 'input_text='$text http://localhost:5000/predict/pneumonia
    input_text = request.form['input_text']
    response = pneumonia_predict(input_text, app.config)
    return response


if __name__ == '__main__':
    app.run()

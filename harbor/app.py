from ris.gastro.model import predict as gastro_predict

from flask import request, Flask

from configparser import ConfigParser

app = Flask(__name__)

app.config.from_pyfile('config.cfg', silent=False)
print(app.config)


@app.route('/predict', methods=['POST'])
def predict():
    print('------------------------------------asssssssssssssssssssssssssssssss')
    print(request.form)
    input_text = request.form['input_text']
    print(input_text)
    print('..................................')
    print(type(input_text))
    response = gastro_predict(input_text, app.config)
    print('..................................')
    print(response)
    return response
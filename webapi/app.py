from flask import Flask, render_template
from ris.gastro.model import predict

app = Flask(__name__)


@app.route('/')
def api_root():
    y_hat = predict('Hello')
    return y_hat, 200


if __name__ == '__main__':
    print('Running server now')
    app.run()

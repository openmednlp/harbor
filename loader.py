from bedrock import common
from os import path
from os import environ

_active_model = None


def load(name):
    shipyard_path = environ['SHIPYARD_DIR']
    pickle_path = path.join(shipyard_path, name)
    global _active_model
    _active_model = common.load_pickle(pickle_path)


if __name__ == '__main__':
    print('Congrats')
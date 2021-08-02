from pycaret.classification import *


model = load_model('assets/ml_models_binaries/NB-final-baseline')


def prediction(data_sample):

    return predict_model(model, data=data_sample)
    
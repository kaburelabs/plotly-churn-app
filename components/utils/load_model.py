from pycaret.classification import *


model = load_model('assets/ml_models_binaries/churn-model-optimized-auc')


def prediction(data_sample):

    return predict_model(model, data=data_sample) 
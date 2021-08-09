from pycaret.classification import *
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, \
                                recall_score, f1_score, confusion_matrix

import numpy as np

# model = load_model('assets/ml_models_binaries/NB-final-baseline')
model = load_model('assets/ml_models_binaries/last-nb-model-2')

def prediction(data_sample):

    return predict_model(model, data=data_sample)
    
# custom metric function
def calculate_profit(y, y_pred):
    tp = np.where((y_pred==1) & (y==1), (5000-1000), 0)
    fp = np.where((y_pred==1) & (y==0), -1000, 0)
    
    return np.sum([tp,fp])

# Calculate scores with Test/Unseen labeled data
def test_score_report(test_df, predict_unseen):
    le = LabelEncoder()
#     test_df["Label"] = le.fit_transform(test_df["Churn Value"].values)
    test_df["Label"] = test_df["Churn Value"].astype(int)
    accuracy = accuracy_score(test_df["Label"], predict_unseen["Label"])
    roc_auc = roc_auc_score(test_df["Label"], predict_unseen["Label"])
    precision = precision_score(test_df["Label"], predict_unseen["Label"])
    recall = recall_score(test_df["Label"], predict_unseen["Label"])
    f1 = f1_score(test_df["Label"], predict_unseen["Label"])
    profit=calculate_profit(test_df["Label"], predict_unseen["Label"])

    df_unseen = pd.DataFrame({
        "Accuracy" : [accuracy],
        "AUC" : [roc_auc],
        "Recall" : [recall],
        "Precision" : [precision],
        "F1 Score" : [f1],
        "Profit":[profit]
    })

    return df_unseen
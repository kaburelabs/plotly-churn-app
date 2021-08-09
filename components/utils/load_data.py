
import pandas as pd
import numpy as np

def create_input_table(input_data):

    name_columns=['CustomerID', 'Gender', 'Senior Citizen', 'Partner',
              'Dependents', 'Tenure Months', 'Phone Service', 'Multiple Lines',
              'Internet Service', 'Online Security', 'Online Backup',
              'Device Protection', 'Tech Support', 'Streaming TV', 'Streaming Movies',
              'Contract', 'Paperless Billing', 'Payment Method', 'Monthly Charges']
    
    data = pd.DataFrame([input_data])
    data.columns = name_columns
    
    return data


def data_transformation(data):
    
    data=data[['CustomerID', 'Gender', 'Senior Citizen', 'Partner',
                     'Dependents', 'Tenure Months', 'Phone Service', 'Multiple Lines',
                     'Internet Service', 'Online Security', 'Online Backup',
                     'Device Protection', 'Tech Support', 'Streaming TV', 'Streaming Movies',
                     'Contract', 'Paperless Billing', 'Payment Method', 'Monthly Charges']].copy()

    data.loc[:,"Multiple Lines"] = np.where(data["Multiple Lines"] == "Yes", 1, 0)
    data.loc[:,"internet"] = np.where(data["Internet Service"] == "No", 0, 1)
    data.loc[:,"Online Security"] = np.where(data["Online Security"] == "Yes", 1, 0)
    data.loc[:,"Online Backup"] = np.where(data["Online Backup"] == "Yes", 1, 0)
    data.loc[:,"Device Protection"] = np.where(data["Device Protection"] == "Yes", 1, 0)
    data.loc[:,"Tech Support"] = np.where(data["Tech Support"] == "Yes", 1, 0)
    data.loc[:,"Streaming TV"] = np.where(data["Streaming TV"] == "Yes", 1, 0)
    data.loc[:,"Streaming Movies"] = np.where(data["Streaming Movies"] == "Yes", 1, 0)
    data.loc[:,"Gender"] = np.where(data["Gender"] == "Male", 1, 0)
    data.loc[:,"Phone Service"] = np.where(data["Phone Service"] == "Yes", 1, 0)

#     data.loc[:,'internet']= np.where(data["Internet Service"] != 'No', 1, 0)

    services = ["Phone Service", "Online Security",
               "Online Backup", "Device Protection", "Tech Support", 
               "Streaming TV", "Streaming Movies", "internet"]

    data.loc[:, 'Total Services'] = (data[services] == 1).sum(axis=1)

    data.loc[:,'Engaged'] = np.where(data['Contract'] != 'Month-to-month', 1,0)

    data.loc[:,'NoProt'] = np.where((data['Online Backup'] != 0) | \
                                       (data['Device Protection'] != 0) | \
                                       (data['Tech Support'] != 0), 1,0)

    data["Senior Citizen"]=np.where(data["Senior Citizen"] == "Yes", 1, 0)
    data["Partner"]=np.where(data["Partner"] == "Yes", 1, 0)
    data["Dependents"]=np.where(data["Dependents"] == "Yes", 1, 0)
    data["Paperless Billing"]=np.where(data["Paperless Billing"] == "Yes", 1, 0)
    
    
    data.loc[:,"payment_automatic"]=[1 if "automatic" in payment_type else 0 for payment_type in data["Payment Method"]]

    return data



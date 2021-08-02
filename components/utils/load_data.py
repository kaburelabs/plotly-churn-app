
import pandas as pd
import numpy as np

def create_input_table(input_data):

    name_columns=['CustomerID', 'City', 'Gender', 'Senior Citizen', 'Partner',
              'Dependents', 'Tenure Months', 'Phone Service', 'Multiple Lines',
              'Internet Service', 'Online Security', 'Online Backup',
              'Device Protection', 'Tech Support', 'Streaming TV', 'Streaming Movies',
              'Contract', 'Paperless Billing', 'Payment Method', 'Monthly Charges']
    
    data = pd.DataFrame([input_data])
    data.columns = name_columns
    
    return data




def data_transformation(data):
    
    data=data[['CustomerID', 'City', 'Gender', 'Senior Citizen', 'Partner',
                     'Dependents', 'Tenure Months', 'Phone Service', 'Multiple Lines',
                     'Internet Service', 'Online Security', 'Online Backup',
                     'Device Protection', 'Tech Support', 'Streaming TV', 'Streaming Movies',
                     'Contract', 'Paperless Billing', 'Payment Method', 'Monthly Charges']]

    data["Multiple Lines"] = np.where(data["Multiple Lines"] == "Yes", 1, 0)
    data["Internet Service"] = np.where(data["Internet Service"] == "No", 0, 1)
    data["Online Security"] = np.where(data["Online Security"] == "Yes", 1, 0)
    data["Online Backup"] = np.where(data["Online Backup"] == "Yes", 1, 0)
    data["Device Protection"] = np.where(data["Device Protection"] == "Yes", 1, 0)
    data["Tech Support"] = np.where(data["Tech Support"] == "Yes", 1, 0)
    data["Streaming TV"] = np.where(data["Streaming TV"] == "Yes", 1, 0)
    data["Streaming Movies"] = np.where(data["Streaming Movies"] == "Yes", 1, 0)

    data['internet']= np.where(data["Internet Service"] != 'No', 'Yes', 'No')

    services = ["Phone Service", "Online Security",
               "Online Backup", "Device Protection", "Tech Support", 
               "Streaming TV", "Streaming Movies", "internet"]

    data['num_services'] = (data[services] == 'Yes').sum(axis=1)

    data.loc[:,'Engaged'] = np.where(data['Contract'] != 'Month-to-month', 1,0)

    data.loc[:,'NoProt'] = np.where((data['Online Backup'] != 'No') | \
                                       (data['Device Protection'] != 'No') | \
                                       (data['Tech Support'] != 'No'), 1,0)

    data["payment_automatic"]=[1 if "automatic" in payment_type else 0 for payment_type in data["Payment Method"]]

    return data

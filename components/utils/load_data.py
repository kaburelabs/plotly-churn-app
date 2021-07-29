
import pandas as pd

def create_input_table(input_data):

    name_columns=['CustomerID', 'City', 'Gender', 'Senior Citizen', 'Partner',
              'Dependents', 'Tenure Months', 'Phone Service', 'Multiple Lines',
              'Internet Service', 'Online Security', 'Online Backup',
              'Device Protection', 'Tech Support', 'Streaming TV', 'Streaming Movies',
              'Contract', 'Paperless Billing', 'Payment Method', 'Monthly Charges',
              'Total Charges']
    
    data = pd.DataFrame([input_data])
    data.columns = name_columns
    
    return data

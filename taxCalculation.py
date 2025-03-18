import pandas as pd
# Function to calculate tax
def taxCalculation(zipCode):
    df = pd.read_csv('/home/codespace/CS-Cart/Tax/taxes.csv')
    return df.loc[df['ZipCode'] == zipCode, 'EstimatedCombinedRate'].values[0]

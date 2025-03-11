import pandas as pd

#Takes area code as input and returns an estimated combined tax rate,
#including local and state taxes if applicable.
#Tax rates are from publicly available databases from Avalara which can be found at taxrates.com
def taxCalculation(zipCode):
    value=zipCode
    df = pd.read_csv('/workspaces/CS-Cart/Tax/taxes.csv')
    print((df.loc[df['ZipCode']==zipCode,'EstimatedCombinedRate']).values[0])
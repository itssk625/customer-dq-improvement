import pandas as pd
def standardize_dobs(df):
    df=df.copy()
    valid=df['is_validdob']
    formatted = df.loc[valid, 'valid_dob'].dt.strftime('%d-%m-%Y')  
    df['valid_dob'] = df['valid_dob'].astype(object)                 
    df.loc[valid, 'valid_dob'] = formatted   
    return df
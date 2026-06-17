import pandas as pd
def standardize_dobs(df):
    df=df.copy()
    valid=df['is_validdob']
    formatted = df.loc[valid, 'cleaned_dob'].dt.strftime('%d-%m-%Y')  
    df['cleaned_dob'] = df['cleaned_dob'].astype(object)                 
    df.loc[valid, 'cleaned_dob'] = formatted   
    return df
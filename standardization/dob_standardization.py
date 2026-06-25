import pandas as pd
def standardize_dobs(df):
    df=df.copy()
    valid=pd.isna(df['dob_issues'])
    formatted = df.loc[valid, 'cleaned_dob'].dt.strftime('%Y-%m-%d')  
    df['cleaned_dob'] = df['cleaned_dob'].astype(object)                 
    df.loc[valid, 'cleaned_dob'] = formatted   
    return df
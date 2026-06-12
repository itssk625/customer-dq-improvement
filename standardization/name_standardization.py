import pandas as pd
import numpy as np
def standardize_names(df):
    df=df.copy()
    df['concatenated_name']=''
    valid=df['is_validname']
    df.loc[valid, 'cleaned_firstname']=df.loc[valid, 'cleaned_firstname'].str[0].str.upper()+df.loc[valid, 'cleaned_firstname'].str[1:].str.lower()
    df.loc[valid, 'cleaned_lastname']=df.loc[valid, 'cleaned_lastname'].str[0].str.upper()+df.loc[valid, 'cleaned_lastname'].str[1:].str.lower()
    df.loc[valid, 'concatenated_name']=df.loc[valid,'cleaned_firstname']+" "+df.loc[valid,'cleaned_lastname']
    df['concatenated_name']=df['concatenated_name'].replace('',np.nan,regex=False)
    return df
    

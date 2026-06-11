import pandas as pd
df=pd.DataFrame({
        'cleaned_firstname': ['John', 'Abdul', 'Preeti', 'Aisha', 'Robert'],
        'cleaned_lastname':  ['Smith', 'Hussain', 'Sharma', 'Ahmed', 'Taylor'],
        'is_validname':      [True, True, True, True, True]
    })
def standardize_names(df):
    df=df.copy()
    df['concatenated_name']=''
    valid=df['is_validname']
    df.loc[valid, 'cleaned_firstname']=df.loc[valid, 'cleaned_firstname'].str[0].str.upper()+df.loc[valid, 'cleaned_firstname'].str[1:].str.lower()
    df.loc[valid, 'cleaned_lastname']=df.loc[valid, 'cleaned_lastname'].str[0].str.upper()+df.loc[valid, 'cleaned_lastname'].str[1:].str.lower()
    df.loc[valid, 'concatenated_name']=df.loc[valid,'cleaned_firstname']+" "+df.loc[valid,'cleaned_lastname']
    return df
    
df=standardize_names(df)
print(df[['concatenated_name']])

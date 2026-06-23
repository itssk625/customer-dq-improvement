import pandas as pd
import numpy as np

def validate_names(df):
    df=df.copy()
    df['name_issues']=''

    df['first_name']=df['first_name'].str.strip()
    df['last_name']=df['last_name'].str.strip()
    emptymask=(pd.isna(df['first_name'])) | (df['first_name']=='') | (pd.isna(df['last_name'])) | (df['last_name']=='')
    df.loc[emptymask, 'name_issues']+='Empty first or last name, '

    df['cleaned_firstname']=(
        df['first_name']
        .fillna('')
        .astype(str)
        .str.replace(r'[^a-zA-Z]','', regex=True)
    )

    df['cleaned_lastname']=(
        df['last_name']
        .fillna('')
        .astype(str)
        .str.replace(r'[^a-zA-Z]','', regex=True)
    )
    invalidmask=((df['cleaned_firstname']=='') | (df['cleaned_lastname']==''))
    df.loc[invalidmask, 'name_issues']+='Invalid name, '

    invalidlength=(((df['cleaned_firstname'].str.len()<3) | (df['cleaned_lastname'].str.len()<3) | (df['cleaned_firstname'].str.len()>50) | (df['cleaned_lastname'].str.len()>50))) 
    df.loc[invalidlength, 'name_issues']+='Name too short or long, '
    
    
    placeholder_names=[
        'test',
        'testing',
        'dummy',
        'unknown',
        'user',
        'null',
        'none'
    ]

    pattern=('|').join(placeholder_names)
    contains_placeholder=((df['cleaned_firstname'].str.contains(pattern, case=False, regex=True, na=False))|(df['cleaned_lastname'].str.contains(pattern, case=False, regex=True, na=False))) 
    df.loc[contains_placeholder, 'name_issues']+='Contains placeholder names, '
    
    keyboard_sequences=[
        'qwerty',
        'asdf',
        'zxcv',
        '12345',
        '123456',
        'qazwsx'
    ]

    pattern=('|').join(keyboard_sequences)
    contains_keyboardseq=((df['cleaned_firstname'].str.contains(pattern, case=False,na=False, regex=True))|df['cleaned_lastname'].str.contains(pattern, case=False, na=False,regex=True))
    df.loc[contains_keyboardseq, 'name_issues']+='Contains keyboard sequences, '

    repletters=((df['cleaned_firstname'].str.match(r'.*([a-zA-Z])\1{4,}.*').fillna(False))|(df['cleaned_lastname'].str.match(r'.*([a-zA-Z])\1{4,}.*')).fillna(False)) 
    df.loc[repletters, 'name_issues']+='Repeated letters'
    df['name_issues']=df['name_issues'].str.strip()
    df['name_issues']=df['name_issues'].str.replace(r',$','',regex=True)
    df['name_issues'] = df['name_issues'].replace('', np.nan)
    valid_mask=pd.isna(df['name_issues'])
    df.loc[valid_mask,'valid_firstname']=df.loc[valid_mask,'cleaned_firstname']
    df.loc[valid_mask, 'valid_lastname']=df.loc[valid_mask, 'cleaned_lastname']
    
    return df

#df=validate_names(df)
#print(df[['firstname','lastname','valid_firstname', 'valid_lastname','is_validname','name_issues']])

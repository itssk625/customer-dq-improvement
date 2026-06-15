import pandas as pd
import numpy as np

'''df = pd.DataFrame({
    'firstname': [
        'John', 'aaaaaaaaaaaaa', 'qwerty123', '', 'Abdul',
        'prEEtI', 'Jane', 'Ali', 'Aisha', '123',
        'Ann1a3', '', '   ', '@Robert', 'Li', None
    ],
    'lastname': [
        'Smith', 'yamada', '', 'dummyy', 'Hussain',
        'shaRMA', 'Doe', 'Khan', 'Ahmed', 'Brown',
        'B', 'Wilson', '', 'Taylor123', 'Wu', 'Johnson'
    ]
})'''

def validate_names(df):
    df=df.copy()
    df['is_validname']=True
    df['name_issue']=''

    df['first_name']=df['first_name'].str.strip()
    df['last_name']=df['last_name'].str.strip()
    emptymask=(pd.isna(df['first_name'])) | (df['first_name']=='') | (pd.isna(df['last_name'])) | (df['last_name']=='')
    df.loc[emptymask, 'is_validname']=False
    df.loc[emptymask, 'name_issue']+='Empty first or last name, '

    df['cleaned_firstname']=(
        df['first_name']
        .astype(str)
        .str.replace(r'[^a-zA-Z]','', regex=True)
    )

    df['cleaned_lastname']=(
        df['last_name']
        .astype(str)
        .str.replace(r'[^a-zA-Z]','', regex=True)
    )
    invalidmask=(((df['cleaned_firstname']=='') | (df['cleaned_lastname']=='') | pd.isna(df['cleaned_firstname']) | pd.isna(df['cleaned_lastname']))) & (df['is_validname'])
    df.loc[invalidmask, 'is_validname']=False
    df.loc[invalidmask, 'name_issue']+='Invalid name, '

    invalidlength=(((df['cleaned_firstname'].str.len()<3) | (df['cleaned_lastname'].str.len()<3) | (df['cleaned_firstname'].str.len()>50) | (df['cleaned_lastname'].str.len()>50))) & (df['is_validname'])
    df.loc[invalidlength, 'is_validname']=False
    df.loc[invalidlength, 'name_issue']+='Name too short or long, '
    
    
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
    df.loc[contains_placeholder, 'is_validname']=False
    df.loc[contains_placeholder, 'name_issue']+='Contains placeholder names, '
    
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
    df.loc[contains_keyboardseq, 'is_validname']=False
    df.loc[contains_keyboardseq, 'name_issue']+='Contains keyboard sequences, '

    repletters=((df['cleaned_firstname'].str.match(r'.*([a-zA-Z])\1{4,}.*').fillna(False))|(df['cleaned_lastname'].str.match(r'.*([a-zA-Z])\1{4,}.*')).fillna(False)) 
    df.loc[repletters, 'is_validname']=False
    df.loc[repletters, 'name_issue']+='Repeated letters'
    
    valid_mask=df['is_validname']
    df.loc[valid_mask,'valid_firstname']=df.loc[valid_mask,'cleaned_firstname']
    df.loc[valid_mask, 'valid_lastname']=df.loc[valid_mask, 'cleaned_lastname']
    df['name_issue']=df['name_issue'].str.strip()
    df['name_issue']=df['name_issue'].str.replace(r',$','',regex=True)
    df['name_issue'] = df['name_issue'].replace('', np.nan)
    return df

#df=validate_names(df)
#print(df[['firstname','lastname','valid_firstname', 'valid_lastname','is_validname','name_issue']])

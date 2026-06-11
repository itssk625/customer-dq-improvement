import pandas as pd
import numpy as np

'''df=pd.DataFrame({'email':['john.doe@example.com',
        'jane.doe@example.com',
        'ali.khan@example.com',
        'aisha.ahmed@example.com',
        '123@example.com',
        'ann1a3@example.com',
        '131413452@example.com',
        '@example.com',
        'john.doe@',
        'john.doe@@example.com',
        'john.doe@.com',
        '',                         # Empty + No @
    '@',                        # Empty username + Empty domain
    '@.com',                    # Empty username + Invalid domain
    'ab@.com',                  # Username too short + Invalid domain
    '12@.com',                  # Username too short + Invalid domain + numeric
    '12345@',                   # Empty domain + Numeric username
    '123456789@example.com',    # Numeric username + Excessive numeric content
    'ab@example.com',           # Username too short
    'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz@example.com',  # Username too long
    '12345678@example.com',     # Numeric username + Excessive numeric content
    'john@@@example.com',       # Multiple @ (before cleaning)
    'john@com',                 # Domain missing dot
    'john@.com',                # Domain starts with dot
    'john@gmail.',              # Domain ends with dot
    '12ab345678@example.com',   # Excessive numeric content
    '___@example.com',          # Weird username but passes many checks
    '111111111@example.com',
    '13asdf4@example.com']})'''

def validate_emails(df):
    df=df.copy()
    df['email_issue']=''
    df['is_validemail']=True
    df['email']=(
        df['email']
        .str.strip()
        .fillna('')
    )

    valid=(df['email'].str.contains(r'@', regex=True, na=False))
    no_separator=~valid
    df.loc[no_separator, 'is_validemail']=False
    df.loc[no_separator, 'email_issue']+='No @ separator, '

    multiple_dots=df['email'].str.contains(r'\.{2,}', regex=True, na=False)
    df.loc[multiple_dots, 'is_validemail']=False
    df.loc[multiple_dots, 'email_issue']+='Multiple ., '
    
    multiple_separator=(df['email'].str.contains(r'@{2,}', regex=True, na=False))|(df['email'].str.count('@')>=2).fillna(False)
    df.loc[multiple_separator,'is_validemail']=False
    df.loc[multiple_separator, 'email_issue']+='Multiple @, '

    df['cleaned_email']=(
        df['email']
        .astype(str)
        .str.replace(r'[^a-zA-Z0-9\.@_]', '', regex=True)
    )
    username=df['cleaned_email'].str.split('@').str[0]
    domain=df['cleaned_email'].str.split('@').str[1]
    emptymask=((pd.isna(username) )| (pd.isna(domain)) | (domain=='') | (username=='')) & ~no_separator & ~multiple_separator
    df.loc[emptymask, 'is_validemail']=False
    df.loc[emptymask, 'email_issue']+='Empty username or domain, '

    invaliddomain=((domain.str.startswith('.'))|(domain.str.endswith('.'))|(~(domain.str.contains(r'\.', regex=True, na=False))))  & ~multiple_separator & ~no_separator
    df.loc[invaliddomain, 'is_validemail']=False
    df.loc[invaliddomain, 'email_issue']+='Incomplete domain, '


    usernamehas_at=username.str.contains(r'@', regex=True)
    df.loc[usernamehas_at, 'is_validemail']=False
    df.loc[usernamehas_at, 'email_issue']+='Username has @, '

    invalidlength=~((username.str.len()>=3) & (username.str.len()<=50)) & (~emptymask)
    df.loc[invalidlength, 'is_validemail']=False
    df.loc[invalidlength, 'email_issue']+='Username too long or short, '

    numericname=(username.str.match(r'^\d+$')) & (username.str.len()>=5)
    df.loc[numericname, 'is_validemail']=False
    df.loc[numericname, 'email_issue']+='Numeric-only username, '
 
    excnumeric=(username.str.count(r'\d')>=8) 
    df.loc[excnumeric, 'is_validemail']=False
    df.loc[excnumeric, 'email_issue']+='Excessive numeric content'

    keyboard_sequences=[
        'qwerty',
        'asdf',
        'zxcv',
        '12345',
        '123456',
        'qazwsx'
    ]

    pattern='|'.join(keyboard_sequences)
    contains_keyboardseq=username.str.contains(
        pattern,
        case=False,
        na=False
    )

    df.loc[contains_keyboardseq, 'is_validemail']=False
    df.loc[contains_keyboardseq, 'email_issue']='Contains keyboard sequences'
    df['email_issue']=df['email_issue'].str.strip()
    df['email_issue']=df['email_issue'].str.replace(r',$','',regex=True)
    df['email_issue']=df['email_issue'].replace('',np.nan)
    valid_mask=df['is_validemail']
    df.loc[valid_mask, 'valid_emails']=df['cleaned_email']
    return df


#df=validate_emails(df)
#print(df[['email','is_validemail','valid_emails','email_issue']])


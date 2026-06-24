import pandas as pd
import numpy as np

def validate_emails(df):
    df=df.copy()
    df['email_issues']=''
    df['email']=(
        df['email']
        .str.strip()
        .fillna('')
    )
    
    emptymask=(df['email']=='')
    df.loc[emptymask, 'email_issues']+='Empty email'

    valid=(df['email'].str.contains(r'@', regex=True, na=False)) 
    no_separator=~valid & ~emptymask
    df.loc[no_separator, 'email_issues']+='No @ separator, '

    multiple_dots=df['email'].str.contains(r'\.{2,}', regex=True, na=False)
    df.loc[multiple_dots, 'email_issues']+='Multiple ., '
    
    multiple_separator=(df['email'].str.count('@')>=2).fillna(False)
    df.loc[multiple_separator, 'email_issues']+='Multiple @, '

    df['cleaned']=(
        df['email']
        .astype(str)
        .str.replace(r'[^a-zA-Z0-9\.@_-]', '', regex=True)
    )
    username=df['cleaned'].str.rsplit('@', n=1).str[0]
    domain=df['cleaned'].str.rsplit('@',n=1).str[1]
    
    emptyusername=((pd.isna(username)) | (username=='')) & (~no_separator) & (~multiple_separator)
    df.loc[emptyusername & ~emptymask, 'email_issues']+='Empty username, '

    emptydomain=((pd.isna(domain)) | (domain=='')) & (~no_separator) & (~multiple_separator)
    df.loc[emptydomain & ~emptymask, 'email_issues']+='Empty domain, '
    
    invaliddomain=((domain.str.startswith('.'))|(domain.str.endswith('.'))|(~(domain.str.contains(r'\.', regex=True, na=False))))  & ~multiple_separator & ~no_separator
    df.loc[invaliddomain & ~emptydomain, 'email_issues']+='Invalid domain, '


    usernamehas_at=username.str.contains('@', regex=False,na=False)
    df.loc[usernamehas_at, 'email_issues']+='Username has @, '
    
    username_dots=(username.str.startswith('.')|username.str.endswith('.')) 
    df.loc[username_dots, 'email_issues']+='Username starts/ends with ., '


    invalidlength=~((username.str.len()>=3) & (username.str.len()<=50)) 
    df.loc[invalidlength & ~emptyusername, 'email_issues']+='Username too long or short, '
    
    
    numericname=(username.str.match(r'^\d+$').fillna(False)) & (username.str.len()>=5)
    df.loc[numericname, 'email_issues']+='Numeric-only username, '
    
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

    df.loc[contains_keyboardseq & ~numericname, 'email_issues']+='Contains keyboard sequences, '
    
    excnumeric=(username.str.count(r'\d')>=8) 
    df.loc[excnumeric & ~numericname, 'email_issues']+='Excessive numeric content, '

    
    df['email_issues']=df['email_issues'].str.strip()
    df['email_issues']=df['email_issues'].str.replace(r',$','',regex=True)
    df['email_issues']=df['email_issues'].replace('',np.nan)
    valid_mask=pd.isna(df['email_issues'])
    df.loc[valid_mask, 'cleaned_email']=df.loc[valid_mask,'cleaned']
    return df





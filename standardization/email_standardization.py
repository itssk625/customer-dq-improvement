import pandas as pd
from rapidfuzz import process
import numpy as np

known_domains=["gmail.com","outlook.com", "yahoo.com","hotmail.com","icloud.com","rediffmail.com","zoho.com","protonmail.com","msn.com"]

domain_typos={"gmail.com": ["gamil.com","gmali.com","gmial.com","gmaill.com","gmal.com","gnail.com",'gmail.com',"gmail.co"],
            "outlook.com": ["outlok.com","outlook.co","outllok.com","outloo.com"],
            "yahoo.com":["yahoo.co","yaho.com","yahooo.com","yyahoo.com","yhoo.com"],
            "hotmail.com":["hotmali.com","hotmail.co","hotmail.con",'hotmal.com',"hotmai.com","hotmial.com"],
            "zoho.com":['zohoo.com'],
            "rediffmail.com":["redifmail.com","rediffmail.co","rediffmali.com","rediffmal.com","rediffmial.com"],
            "protonmail.com":["protoonmail.com","protonmail.co","protnmail.com","prtonmai.com"],
            "icloud.com":["icloud.con"]
            }

domain_typos_flat={
    typo:canonical
    for canonical, typos in domain_typos.items()
    for typo in typos
}
def standardize_emails(df):
    df=df.copy()
    mask=df['is_validemail']
    df['email_issue']=df['email_issue'].fillna('')
    df.loc[mask,'valid_emails']=df.loc[mask,'valid_emails'].str.lower()
    df['domain']=df['valid_emails'].str.split('@').str[1]
    exactchk=df['domain'].isin(known_domains)
    df.loc[exactchk & mask,'suggested_domain']=df.loc[exactchk & mask,'domain']
    df.loc[~exactchk & mask, 'suggested_domain']=df.loc[~exactchk & mask,'domain'].map(domain_typos_flat)
    unrecognized_domain=pd.isna(df['suggested_domain'])
    df.loc[unrecognized_domain & mask,"suggested_domain"]=df.loc[unrecognized_domain & mask,"domain"] 
    df['email_issue']=df['email_issue'].str.strip()
    df['email_issue']=df['email_issue'].str.rstrip(',')
    df['email_issue']=df['email_issue'].replace('',np.nan)
    print(df[['email','email_issue','domain','suggested_domain']])
    return df
    
#df=standardize_emails(df)
#print(df[['email','email_issue','suggested_domain']])
    





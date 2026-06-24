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
    mask=pd.isna(df['email_issues'])
    df['email_issues']=df['email_issues'].fillna('')
    df.loc[mask,'cleaned_email']=df.loc[mask,'cleaned_email'].str.lower()
    df['domain']=df['cleaned_email'].str.split('@').str[1]
    exactchk=df['domain'].isin(known_domains)
    df.loc[exactchk & mask,'extracted_domain']=df.loc[exactchk & mask,'domain']
    df.loc[~exactchk & mask, 'extracted_domain']=df.loc[~exactchk & mask,'domain'].map(domain_typos_flat)
    unrecognized_domain=pd.isna(df['extracted_domain'])
    df.loc[unrecognized_domain & mask,"extracted_domain"]=df.loc[unrecognized_domain & mask,"domain"] 
    df.loc[mask, "cleaned_email"]=df.loc[mask, "cleaned_email"].str.split("@").str[0]+"@"+df.loc[mask, "extracted_domain"]
    df['email_issues']=df['email_issues'].str.strip()
    df['email_issues']=df['email_issues'].str.rstrip(',')
    df['email_issues']=df['email_issues'].replace('',np.nan)
    return df
    
#df=standardize_emails(df)
#print(df[['email','email_issues','extracted_domain']])
    





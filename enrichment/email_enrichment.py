import pandas as pd
import numpy as np
with open('../disposable_email_blocklist.conf') as blocklist:
    blocklist_content = {line.rstrip() for line in blocklist.readlines()}

known_domains={"gmail.com","outlook.com", "yahoo.com","hotmail.com","icloud.com","rediffmail.com","zoho.com","protonmail.com","msn.com"}

def enrich_emails(df):
    df=df.copy()
    df['email_issues']=df['email_issues'].fillna('')
    mask=(pd.isna(df['extracted_domain']))|(df['extracted_domain']=='')
    df['is_disposable_email']=False
    for idx in df[~mask].index:
        domain_parts = df.loc[idx,'extracted_domain'].split(".")
        for i in range(len(domain_parts)):
            if ".".join(domain_parts[i:]) in blocklist_content:
                df.loc[idx,'is_disposable_email']=True
                break
    disposable_invalid=df['is_disposable_email']
    df.loc[disposable_invalid, 'is_validemail']=False
    df.loc[disposable_invalid, 'email_issues']+='Disposable email'
    mask=(~(df['is_disposable_email']) & ((df['extracted_domain']).notna()) & (df['extracted_domain']!=''))
    for idx in df[mask].index:
        if (df.loc[idx, 'extracted_domain'] in known_domains):
            df.loc[idx,'email_classified_as']='Personal'
        else:
            df.loc[idx,'email_classified_as']='Business'
    df.loc[disposable_invalid,'cleaned_email']=np.nan
    df['email_issues']=df['email_issues'].str.strip()
    df['email_issues']=df['email_issues'].str.rstrip(',')
    df['email_issues']=df['email_issues'].replace('', np.nan)
    return df



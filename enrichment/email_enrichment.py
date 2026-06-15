import pandas as pd
import numpy as np
with open('../disposable_email_blocklist.conf') as blocklist:
    blocklist_content = {line.rstrip() for line in blocklist.readlines()}
df=pd.DataFrame({'domain': [
        "gmail.com",
        "yahoo.com",
        "outlook.com",

        "10minutemail.com",
        "mailinator.com",
        "guerrillamail.com",

        "sub.hehe.mailinator.com",
        "test.10minutemail.com",

        "tempmail.org",
        "dispostable.com",

        "company.co.uk",
        "google.com",
        "mit.edu",

        None,
        "",
        None
    ]
})

known_domains=["gmail.com","outlook.com", "yahoo.com","hotmail.com","icloud.com","rediffmail.com","zoho.com","protonmail.com","msn.com"]

def enrich_emails(df):
    df=df.copy()
    mask=(pd.isna(df['suggested_domain']))|(df['suggested_domain']=='')
    df['is_disposable']=False
    for idx in df[~mask].index:
        domain_parts = df.loc[idx,'suggested_domain'].split(".")
        for i in range(len(domain_parts)):
            if ".".join(domain_parts[i:]) in blocklist_content:
                df.loc[idx,'is_disposable']=True
                break
    mask=(~(df['is_disposable']) & ((df['suggested_domain']).notna()) & (df['suggested_domain']!=''))
    for idx in df[mask].index:
        if (df.loc[idx, 'suggested_domain'] in known_domains):
            df.loc[idx,'email_type']='Personal'
        else:
            df.loc[idx,'email_type']='Business'

    print(df[['suggested_domain','is_disposable','email_type']])
    return df



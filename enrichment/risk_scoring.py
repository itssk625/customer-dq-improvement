import pandas as pd
import numpy as np

def email_risk(issue):
    if (pd.notna(issue)):
        return 14
    return 0
    
def phoneno_risk(issue):
    if (pd.notna(issue)):
        return 14
    return 0
    
def name_risk(issue):
    if (pd.notna(issue)):
        return 10
    return 0
    
def dob_risk(issue):
    if (pd.notna(issue)):
        return 14
    return 0
    
def nationality_risk(issue):
    if (pd.notna(issue)):
        return 24
    return 0
    
def score_risk(df):
    df=df.copy()
    duplc_emails=df['cleaned_email'].duplicated(keep=False)
    df['is_emailduplicate']=(duplc_emails & df['cleaned_email'].notna())
    duplc_phones=df['cleaned_phoneno'].duplicated(keep=False)
    df['is_phoneduplicate']=(duplc_phones & df['cleaned_phoneno'].notna())
    for idx in df.index:
        score=0
        score+=email_risk(df.loc[idx, "email_issues"])
        score+=phoneno_risk(df.loc[idx, "phoneno_issues"])
        score+=name_risk(df.loc[idx, "name_issues"])
        score+=dob_risk(df.loc[idx, "dob_issues"])
        score+=nationality_risk(df.loc[idx, "nationality_issue"])
        if (df.loc[idx, 'is_emailduplicate'] or df.loc[idx,'is_phoneduplicate']):
            score+=10
        df.loc[idx, "risk_score"]=int(score)
    return df
        
        

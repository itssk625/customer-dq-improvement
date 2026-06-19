import pandas as pd
import numpy as np
fields=["email_issues", "phoneno_issues","name_issues", "dob_issues", "nationality_issue"]

nationality_risks={
    "No nationality provided": 5,
    "Invalid nationality": 5,
    "Unknown nationality": 5
}

dob_risks={
    "Empty DOB": 5,
    "Future DOB": 5,
    "Unrealistic age > 100 years": 5,
    "Invalid format or date": 5,
}

name_risks={
    'Empty first or last name': 20, 
    'Repeated letters': 5,
    'Contains keyboard sequences': 10,
    'Invalid name': 20,
    'Name too short or long': 20,
    'Contains placeholder names': 10
}

email_risks={
    'Invalid domain': 20,
    'Empty domain': 20,
    'Empty username': 20,
    'Empty email': 20,
    'No @ separator': 20,

    'Multiple @': 20,
    'Multiple .': 20,
    'Numeric-only username': 20,
    'Username too long or short': 20,
    'Username has @': 20,

    'Excessive numeric content': 20,
    'Contains keyboard sequences': 20,
    'Username starts/ends with .': 20
}

phoneno_risks={
    "All zeroes phone number": 20,
    "Invalid length": 20,
    "Unknown country code": 20,
    "Invalid country code": 20,
    "Empty subscriber number": 20,
    "Empty mobile number": 20,
    "Repeating digits phone number": 20,

    "Leading zeroes phone number": 20,
    "Trailing zeroes phone number": 20,
}


def email_risk(issue):
    if (pd.notna(issue)):
        issues=[i.strip() for i in issue.split(",")]
        return max([email_risks.get(i, 0) for i in issues], default=0)
    return 0
    
def phoneno_risk(issue):
    if (pd.notna(issue)):
        issues=[i.strip() for i in issue.split(",")]
        return max([phoneno_risks.get(i, 0) for i in issues], default=0)
    return 0
    
def name_risk(issue):
    if (pd.notna(issue)):
        issues=[i.strip() for i in issue.split(",")]
        return max([name_risks.get(i, 0) for i in issues], default=0)
    return 0
    
def dob_risk(issue):
    s=0
    if (pd.notna(issue)):
        return dob_risks.get(issue, 0)
    return s
    
def nationality_risk(issue):
    s=0
    if (pd.notna(issue)):
        return nationality_risks.get(issue, 0)
    return s
    
def score_risk(df):
    df=df.copy()
    duplc_emails=df['cleaned_email'].duplicated(keep=False)
    df['is_emailduplicate']=(duplc_emails & df['is_validemail'])
    duplc_phones=df['cleaned_phoneno'].duplicated(keep=False)
    df['is_phoneduplicate']=(duplc_phones & df['is_validphoneno'])
    for idx in df.index:
        score=0
        score+=email_risk(df.loc[idx, "email_issues"])
        score+=phoneno_risk(df.loc[idx, "phoneno_issues"])
        score+=name_risk(df.loc[idx, "name_issues"])
        score+=dob_risk(df.loc[idx, "dob_issues"])
        score+=nationality_risk(df.loc[idx, "nationality_issue"])
        if (df.loc[idx, 'is_emailduplicate'] or df.loc[idx,'is_phoneduplicate']):
            score+=20
        df.loc[idx, "risk_score"]=int(score)
        print(type(score))
    return df
        
        

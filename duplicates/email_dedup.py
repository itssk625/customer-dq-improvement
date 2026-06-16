import pandas as pd
import numpy as np

df = pd.DataFrame({
    "record_id": [1, 2, 3, 4, 5],

    "concatenated_name": [
        "John Doe",
        np.nan,
        "John Doe",
        "Alice Smith",
        "Bob Khan"
    ],
    "is_validname": [True, False, True, True, True],
    "name_issue": [
        np.nan,
        "Missing first name",
        np.nan,
        np.nan,
        np.nan
    ],

    "valid_dob": [
        "1999-01-01",
        "1999-01-01",
        np.nan,
        "2000-05-10",
        "1998-08-20"
    ],
    "is_validdob": [True, True, False, True, True],
    "dob_issue": [
        np.nan,
        np.nan,
        "Invalid DOB",
        np.nan,
        np.nan
    ],

    "valid_emails": [
        "john@gmail.com",
        "john@gmail.com",
        "john@gmail.com",
        "alice@gmail.com",
        "bob@yahoo.com"
    ],
    "is_validemail": [True, True, True, True, True],
    "email_issue": [np.nan] * 5,
    "is_disposable": [False] * 5,
    "email_type": [
        "Personal",
        "Personal",
        "Personal",
        "Personal",
        "Personal"
    ],
    "suggested_domain": [
        "gmail.com",
        "gmail.com",
        "gmail.com",
        "gmail.com",
        "yahoo.com"
    ],

    "valid_phone": [
        np.nan,
        "919876543210",
        "919999999999",
        "918888888888",
        "917777777777"
    ],
    "is_validphoneno": [False, True, True, True, True],
    "phoneno_issues": [
        "Missing phone",
        np.nan,
        np.nan,
        np.nan,
        np.nan
    ],
    "extracted_country": [
        np.nan,
        "India",
        "India",
        "India",
        "India"
    ],
    "extracted_operator": [
        np.nan,
        "Airtel",
        "Jio",
        "Vodafone",
        "Airtel"
    ],

    "valid_nationality": [
        "India",
        np.nan,
        "India",
        "USA",
        "Pakistan"
    ],
    "is_validnationality": [
        True,
        False,
        True,
        True,
        True
    ],
    "nationality_issue": [
        np.nan,
        "Unknown nationality",
        np.nan,
        np.nan,
        np.nan
    ],

    "gender": [
        "Male",
        "Male",
        "Male",
        "Female",
        "Male"
    ]
})

print(df)
related_fields={
    "concatenated_name": ["is_validname","name_issue"],
    "valid_dob":["is_validdob", "dob_issue"],
    "valid_emails":["is_validemail", "email_issue", "is_disposable", "email_type", "suggested_domain"],
    "valid_phone": ["is_validphoneno", "phoneno_issues", "extracted_country", "extracted_operator"],
    "valid_nationality":["is_validnationality", "nationality_issue"],
    "gender":[]
                
}
def dedup_emails_upload(df):
    df=df.copy()
    duplc_emails=df['valid_emails'].duplicated(keep=False)
    df['is_emailduplicate']=(duplc_emails & df['is_validemail'])
    print(df[['valid_emails','is_validemail','is_emailduplicate']])
    emails=df['valid_emails'].dropna().unique()
    candidates=[]
    #consider all the fields reqd in the master table to create
    fields=['concatenated_name', 'valid_dob', 'valid_emails', 'valid_phone', 'valid_nationality',  'gender']
    for email in emails:
        group=df[df['valid_emails']==email]
        if (len(group)>1): 
            record={}
            for field in fields:
                for idx in group.index:
                    if field not in record and pd.notna(df.loc[idx, field]):
                        record[field]=df.loc[idx, field]
                        for f in related_fields[field]:
                            record[f]=df.loc[idx, f]
            candidates.append(record)
                        
        else:
            idx=group.index[0]
            record=df.loc[idx].to_dict()
            candidates.append(record)
    
    master_candidates=pd.DataFrame(candidates)    
    print(master_candidates)
    return master_candidates

def merge_emails_master(df):
    df=df.copy()
    
    return df

df=dedup_emails_upload(df)
merge_emails_master(df)

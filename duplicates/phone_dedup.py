import pandas as pd

df = pd.DataFrame({
    "record_id": [1, 2, 3, 4, 5, 6],
    "valid_emails": [
        "john@gmail.com",
        "anna@gmail.com",
        "john@gmail.com",      # duplicate email
        "ali@yahoo.com",
        "priya@gmail.com",
        "ali@yahoo.com"        # duplicate email
    ],
    "valid_phone": [
        "919876543210",
        "919999999999",
        "919876543210",        # duplicate phone
        "441234567890",
        "971501234567",
        "441234567890"         # duplicate phone
    ],
    "is_validemail": [True]*6,
    "is_validphoneno": [True]*6
})


def dedup_phones(df):
    df=df.copy()
    duplc_phones=df['valid_phone'].duplicated(keep=False)
    df['is_phoneduplicate']=(duplc_phones & df['is_validphoneno'])
    print(df[['valid_phone','is_validphoneno','is_phoneduplicate']])
    return df

dedup_phones(df)
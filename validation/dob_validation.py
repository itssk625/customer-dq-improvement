import pandas as pd
import numpy as np
from datetime import datetime

#df=pd.DataFrame({'dob':[' 12a-05-1990  ','31/12/1985','    1995-07-20 ','2000/01/15','/////15.08.1988','/29-02-2001','30/02/1999','1990-13-01','1990/00/10','15-08-1880','15-08-2026',None,'abc']})
formats=['%d-%m-%Y','%d/%m/%Y','%Y-%m-%d','%Y/%m/%d', '%d.%m.%Y','%d-%m-%y','%d/%m/%y']

def validate_dobs(df):
    df=df.copy()
    emptymask=pd.isna(df['dob'])|(df['dob'].str.strip()=='')
    df.loc[emptymask, 'dob_issues']='Empty DOB'
    df['clean_dob']=(
            df['dob']
            .astype(str)
            .str.strip()
            .str.replace(r'[^0-9\.\/-]','', regex=True)
            .str.replace(r'\.{2,}','.',regex=True)
            .str.replace(r'\/{2,}','/', regex=True)
            .str.replace(r'-{2,}','-', regex=True)
            .str.replace(r'^[\.\/\-]+', '',regex=True)
            .str.replace(r'[\.\/\-]+$','', regex=True)
    )
    df['parsed_dob']=pd.NaT
    for fmt in formats:
        mask=pd.isna(df['parsed_dob'])
        df.loc[mask,'parsed_dob']=pd.to_datetime(df['clean_dob'],format= fmt,errors='coerce')
                    
    invalid_date=pd.isna(df['parsed_dob']) & ~emptymask
    df.loc[invalid_date, 'dob_issues']='Invalid format or date'

    future_date=(df['parsed_dob'].notna() & df['parsed_dob']>pd.Timestamp.today()) 
    df.loc[future_date, 'dob_issues']='Future DOB'

    unrealistic_age=(df['parsed_dob'].notna() & (pd.Timestamp.today()-df['parsed_dob']).dt.days>36525)
    df.loc[unrealistic_age, 'dob_issues']='Unrealistic age > 100 years'

    valid_mask=pd.isna(df['dob_issues'])
    df.loc[valid_mask,'cleaned_dob']=df['parsed_dob']
    df.loc[valid_mask,'cleaned_dob']=pd.to_datetime(df.loc[valid_mask,'cleaned_dob'],errors="coerce")
    return df

#df=validate_dobs(df)
#print(df[['dob','cleaned_dob','parsed_dob','cleaned_dob','is_validdob','dob_issues']])
import pandas as pd
import os
standardize={
    'm':'male', 'f':'female', 'other': 'others', 'o':'others', 'nonbinary': 'others','t': 'others','nb': 'others','transgender':'others', 'prefernottosay':'others'
    
}

genders=['male','female','others']
def standardize_gender(df):
    df=df.copy()
    emptymask=(pd.isna(df['gender'])) | (df['gender'].str.strip()=='')
    df.loc[emptymask, 'gender_issues']="No gender provided"
    df['cleaned_gender']=(
        df['gender']
        .str.strip()
        .str.lower()
        .str.replace(r'[^a-z]','', regex=True)
    )
    mask=(df['cleaned_gender'].notna()) & (~(df['cleaned_gender'].isin(genders)))
    df.loc[mask, 'cleaned_gender']=df.loc[mask, 'cleaned_gender'].map(standardize)
    mask=df['cleaned_gender'].notna()
    df.loc[mask, 'cleaned_gender']=df.loc[mask, 'cleaned_gender'].str.title()
    df.loc[~mask & ~emptymask, 'gender_issues']='Invalid gender'
    print(df[['gender','cleaned_gender','gender_issues']])
    return df


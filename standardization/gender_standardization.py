import pandas as pd
import os
standardize={
    'm':'male', 'f':'female', 'other': 'others', 'o':'others', 'non-binary': 'others','t': 'others','nb': 'others','transgender':'others', 'prefer not to say':'others'
    
}
genders=['male','female','others']
def standardize_gender(df):
    df=df.copy()
    emptymask=pd.isna(df['gender'])
    df.loc[]
    df['gender']=(
        df['gender']
        .str.strip()
        .str.lower()
        .str.replace(r'[^a-z]','', regex=True)
    )
    mask=(df['gender'].notna() & ~df['gender'].isin(genders))
    df.loc[mask, 'gender']=df.loc[mask, 'gender'].map(standardize)
    mask=df['gender'].notna()
    df.loc[mask, 'gender']=df.loc[mask, 'gender'].str.title()
    return df


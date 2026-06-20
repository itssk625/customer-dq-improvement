import pandas as pd
import numpy as np
from db.connection import get_connection

name_issue={
    'Empty first or last name': 20, 
    'Repeated letters': 5,
    'Contains keyboard sequences': 10,
    'Invalid name': 20,
    'Name too short or long': 20,
    'Contains placeholder names': 10
}

def email_score(issue):
    if(pd.isna(issue)):
        return 25
    return 0
    
def phoneno_score(issue):
    if (pd.isna(issue)):
        return 25
    return 0
    
def name_score(issue):
    if (pd.isna(issue)):
        return 20
    issues=[i.strip() for i in issue.split(",")]
    return (20-max([name_issue.get(i, 0) for i in issues], default=0))

    
def dob_score(issue):
    if (pd.isna(issue)):
        return 10
    return 0
    
def nationality_score(issue):
    if (pd.isna(issue)):
        return 15
    return 0
    
def gender_score(val):
    if (pd.notna(val)):
        return 5
    return 0

def score_dq():
    conn=get_connection()
    df=pd.read_sql_query("SELECT cleaned_email, name_issues, dob_issues, email_issues, phoneno_issues, nationality_issue, is_disposable_email, gender FROM MASTER_CUSTOMER_email", conn)
    df=df.copy()
    cursor=conn.cursor()
    for idx in df.index:
        score=0
        score+=email_score(df.loc[idx, "email_issues"])
        if (df.loc[idx, 'is_disposable_email']):
            if (score==25):
                score-=10
        score+=phoneno_score(df.loc[idx, 'phoneno_issues'])
        score+=name_score(df.loc[idx, "name_issues"])
        score+=dob_score(df.loc[idx, 'dob_issues'])
        score+=nationality_score(df.loc[idx, "nationality_issue"])
        score+=gender_score(df.loc[idx, 'gender'])
        df.loc[idx, "dq_score"]=score
        email=df.loc[idx, "cleaned_email"]
        
        query=f"""
        UPDATE master_customer_email SET dq_score=%s WHERE cleaned_email=%s
        """
        cursor.execute(query, (int(score), email))
    conn.commit()
    
    df=pd.read_sql_query("SELECT cleaned_phoneno, name_issues, dob_issues, email_issues, phoneno_issues, nationality_issue, is_disposable_email, gender from master_customer_phone", conn)
    df=df.copy()
    for idx in df.index:
        score=0
        score+=email_score(df.loc[idx, 'email_issues'])
        if (df.loc[idx, 'is_disposable_email']):
            if (score==25):
                score-=10
        score+=phoneno_score(df.loc[idx, 'phoneno_issues'])
        score+=name_score(df.loc[idx, 'name_issues'])
        score+=dob_score(df.loc[idx, 'dob_issues'])
        score+=nationality_score(df.loc[idx, 'nationality_issue'])
        score+=gender_score(df.loc[idx, 'gender'])
        df.loc[idx, 'dq_score']=score
        phoneno=df.loc[idx,'cleaned_phoneno']
        query=f"""
        UPDATE master_customer_phone set dq_score=%s where cleaned_phoneno=%s
        """
        cursor.execute(query, (int(score), phoneno))
    conn.commit()
    cursor.close()
    conn.close()
        
    
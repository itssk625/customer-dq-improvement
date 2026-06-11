import pandas as pd
from validation.dob_validation import validate_dobs
from validation.name_validation import validate_names
from validation.email_validation import validate_emails
from validation.phone_validation import validate_phones
#from standardization.dob_standardization import standardize_dob
#from standardization.name_standardization import standardize_names
#from standardization.email_standardization import standardize_emails
#from standardization.phone_standardization import standardize_phones
#from standardization.country_standardization import standardize_country
#from enrichment.email_enrichment import enrich_emails
#from enrichment.phone_enrichment import enrich_phones
#from enrichment.risk_scoring import score_risk
from db.connection import get_connection

def main():
    try:
        conn=get_connection()
        print("Database connected successfully!")
        cursor=conn.cursor()
        cursor.execute("SELECT current_database();")
        print(cursor.fetchone())
        cursor.close()
        conn.close()
        '''
        df=pd.read_csv("data.csv")

        #validation
        df=validate_names(df)
        df=validate_dobs(df)
        df=validate_phones(df)
        df=validate_emails(df)
        return df
        #standardization
        df=standardize_names(df)
        df=standardize_dob(df)
        df=standardize_phones(df)
        df=standardize_emails(df)
        df=standardize_country(df)


        #enrichment
        df=enrich_phones(df)
        df=enrich_emails(df)
        df=score_risk(df)

        #write to cleaned customer records

        #deduplication
        df=deduplicate(df)

        #scoring
        df=dq_scoring(df)

        #write to master table

        #calculate report metrics
        df=calc_reportmetrics(df)
        #calculate master table metrics
        df=calc_dashboardmetrics(df)'''
    except Exception as e:
        print("Error:", e)
        
    
if __name__=='__main__':
    main()
    #df=main()
    #print(df)
    #print(df[['dob','cleaned_dob','parsed_dob','valid_dob','is_validdob','dob_issue']])
    #print(df[['firstname','lastname','is_validname','name_issue']])
    #print(df[['email','is_validemail','valid_emails','email_issue']])
    #print(df[[ "phoneno", "code","cleaned_phone","is_validphoneno","phoneno_issues"]])

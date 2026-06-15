import pandas as pd
from validation.dob_validation import validate_dobs
from validation.name_validation import validate_names
from validation.email_validation import validate_emails
from validation.phone_validation import validate_phones
from standardization.dob_standardization import standardize_dobs
from standardization.name_standardization import standardize_names
from standardization.email_standardization import standardize_emails
#from standardization.phone_standardization import standardize_phones
from standardization.country_standardization import standardize_country
from enrichment.email_enrichment import enrich_emails
from enrichment.phone_enrichment import enrich_phones
#from enrichment.risk_scoring import score_risk
from db.connection import get_connection
from io import StringIO

def main():
    try:
       
        df=pd.read_csv("./data/data.csv")
        conn=get_connection()
        cursor=conn.cursor()
        with open("./data/data.csv","r") as f:
            cursor.copy_expert(
                """
                COPY raw_customer_records
                (
                    first_name,
                    last_name,
                    dob,country,gender,email,phone_no
                    
                )
                FROM STDIN
                WITH CSV HEADER;
                """, f
            )
            conn.commit()
        df=pd.read_sql_query(
            "SELECT * FROM raw_customer_records", conn
        )
        
        print(df)
        
        #validation
        df=validate_names(df)
        df=validate_dobs(df)
        df=validate_phones(df)
        df=validate_emails(df)
        
        
        #standardization
        df=standardize_names(df)
        df=standardize_dobs(df)
        #df=standardize_phones(df)
        df=standardize_emails(df)
        df=standardize_country(df)
        df=enrich_emails(df)
        df=enrich_phones(df)
       
        
        print(df[['dob','cleaned_dob','parsed_dob','valid_dob','is_validdob','dob_issue']])
        print(df[['first_name','last_name','is_validname','name_issue']])
        print(df[['email','email_issue','suggested_domain']])
        print(df[["phone_no", "valid_phone","code","subscriber_number","phoneno_issues"]])
        print(df[['valid_nationality','nationality_issue']])
        
        df=df[['record_id', 'file_id', 'concatenated_name','valid_dob', 'valid_emails','valid_phone',  'valid_nationality','is_validname', 'is_validdob', 'is_validemail','is_validphoneno','is_validnationality','name_issue','dob_issue', 'email_issue','phoneno_issues', 'is_disposable','email_type','suggested_domain', 'extracted_country','gender','iso_code','nationality_issue']]
        
        
        buffer=StringIO()
        df.to_csv(buffer, index=False, header=False)
        buffer.seek(0)
        cursor.copy_expert(
            """
            COPY cleaned_customer_records(
                record_id, file_id, cleaned_name,
                cleaned_dob,cleaned_email,cleaned_phoneno,standardized_country,
                is_validname,is_validdob,is_validemail,is_validphoneno,is_validcountry,
                name_issues,dob_issues,email_issues,phoneno_issues,is_disposable_email,
                email_classified_as,extracted_domain, extracted_country,
                gender,iso_code,nationality_issue
            )
            FROM STDIN
            WITH CSV
            """, buffer
            
        )
        conn.commit()
        return df
        '''
        #enrichment
        return df
        
        df=score_risk(df)

        #write to cleaned customer records

        #deduplication
        df=deduplicate(df)

        #scoring
        df=dq_scoring(df)

        #write to master table

        #calculate report metrics
        df=calculate_reportmetrics(df)
        #calculate master table metrics
        df=calculate_dashboardmetrics(df)'''
    except Exception as e:
        print("Error:", e)
        
    
if __name__=='__main__':
    df=main()
    

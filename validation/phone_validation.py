import pandas as pd
import numpy as np

country_codes = {
    "1",    # USA, Canada
    "7",    # Russia
    "20",   # Egypt
    "27",   # South Africa
    "30",   # Greece
    "31",   # Netherlands
    "32",   # Belgium
    "33",   # France
    "34",   # Spain
    "39",   # Italy
    "41",   # Switzerland
    "43",   # Austria
    "44",   # United Kingdom
    "45",   # Denmark
    "46",   # Sweden
    "47",   # Norway
    "48",   # Poland
    "49",   # Germany

    "51",   # Peru
    "52",   # Mexico
    "54",   # Argentina
    "55",   # Brazil
    "56",   # Chile
    "57",   # Colombia
    "58",   # Venezuela

    "60",   # Malaysia
    "61",   # Australia
    "62",   # Indonesia
    "63",   # Philippines
    "64",   # New Zealand
    "65",   # Singapore
    "66",   # Thailand

    "81",   # Japan
    "82",   # South Korea
    "84",   # Vietnam
    "86",   # China

    "90",   # Turkey
    "91",   # India
    "92",   # Pakistan
    "93",   # Afghanistan
    "94",   # Sri Lanka
    "95",   # Myanmar
    "98",   # Iran

    "212",  # Morocco
    "213",  # Algeria
    "216",  # Tunisia
    "218",  # Libya

    "220",  # Gambia
    "221",  # Senegal
    "233",  # Ghana
    "234",  # Nigeria
    "254",  # Kenya
    "255",  # Tanzania
    "256",  # Uganda

    "351",  # Portugal
    "352",  # Luxembourg
    "353",  # Ireland
    "354",  # Iceland
    "357",  # Cyprus

    "380",  # Ukraine
    "385",  # Croatia
    "386",  # Slovenia
    "387",  # Bosnia

    "852",  # Hong Kong
    "853",  # Macau
    "855",  # Cambodia
    "856",  # Laos
    "880",  # Bangladesh
    "886",  # Taiwan

    "960",  # Maldives
    "961",  # Lebanon
    "962",  # Jordan
    "963",  # Syria
    "964",  # Iraq
    "965",  # Kuwait
    "966",  # Saudi Arabia
    "967",  # Yemen
    "968",  # Oman
    "970",  # Palestine
    "971",  # UAE
    "972",  # Israel
    "973",  # Bahrain
    "974",  # Qatar
    "975",  # Bhutan
    "976",  # Mongolia
    "977",  # Nepal
}


def validate_phones(df):
    df=df.copy()
    df['phoneno_issues']=''
    emptymask = (
        pd.isna(df["phone_no"]) | (df["phone_no"].str.strip() == "")
    ).fillna(False)
    df.loc[emptymask, "phoneno_issues"]+= "Empty mobile number"
    
    multimask = df["phone_no"].fillna("").str.split(",").str.len() > 1
    df.loc[multimask, "phone_no"] = df.loc[multimask, "phone_no"].str.split(",").str[0]
    df["phone_no"]=df["phone_no"].str.strip()
    sep_mask = df["phone_no"].str.match(r"^\+?\d{1,}[\ -]").fillna(False)
    known_code = ~emptymask & (sep_mask)
    unknown_code = (~emptymask & ~sep_mask)  
    
    parts = df['phone_no'].str.split(r'[ -]', n=1)
    df.loc[known_code & sep_mask, "code"] =  parts.str[0].str.replace(r'[^\d]','',regex=True)
    df.loc[known_code & sep_mask, "subscriber_number"] = parts.str[1].str.replace(' ', '')
    
    df.loc[unknown_code,'subscriber_number']=(
        df.loc[unknown_code, 'phone_no']
        .str.strip()
        .str.replace(r"[^0-9]", "", regex=True)
    )
    
    setcode=df['subscriber_number'].isin(country_codes)
    df.loc[setcode,'code']=df.loc[setcode,'subscriber_number']
    df.loc[setcode, 'subscriber_number']=np.nan
    

    unknown_code = (~emptymask & ~sep_mask & ~setcode)
    
    empty_subscriber=(pd.isna(df['subscriber_number']))|(df['subscriber_number']=='')
    df.loc[empty_subscriber & ~emptymask, 'phoneno_issues']+='Empty subscriber number, '
    
    is_validcodes = ((df["code"].str.len() <= 3)
    & (df["code"].str.len() > 0)
    & (df["code"].isin(country_codes))
    ).fillna(False)
    df.loc[(~is_validcodes & known_code) | unknown_code, "phoneno_issues"]+= "Invalid country code, "

    df.loc[~emptymask, "cleaned"] = (
    df.loc[~emptymask, "phone_no"]
    .astype(str)
    .str.strip()
    .str.replace(r"[^0-9]", "", regex=True)
    ) 

    lengthmask = ((df["cleaned"].str.len() < 8) | (df["cleaned"].str.len() > 18)) & (~emptymask)
    df.loc[lengthmask & ~empty_subscriber, "phoneno_issues"]+= "Invalid length, "
   
    df['checked_number']=np.where(((pd.isna(df['code']))|(df['code']=='')),df['cleaned'], df['subscriber_number'])
  
    df['checked_number']=(
        df['checked_number']
        .str.strip()
        .str.replace(r"[^0-9]", "", regex=True)
    )
    
    allzero = df["checked_number"].str.match(r"^0+$").fillna(False)
    df.loc[~emptymask & allzero & ~empty_subscriber, "phoneno_issues"]+= "All zeroes phone number"

    leadzero = df["checked_number"].str.match(r"^0{4,}\d+$").fillna(False) & ~allzero
    df.loc[~emptymask & leadzero & ~empty_subscriber, "phoneno_issues"]+= "Leading zeroes phone number, "

    trailzero = df["checked_number"].str.match(r"^\d+0{4,}$").fillna(False) & ~allzero
    df.loc[~emptymask & trailzero & ~empty_subscriber, "phoneno_issues"]+= "Trailing zeroes phone number, "
 
    repdig = df["checked_number"].str.match(r"^(\d)\1+$").fillna(False) & ~allzero
    df.loc[~emptymask & repdig & ~empty_subscriber, "phoneno_issues"]+= "Repeating digits phone number"
    df['phoneno_issues']=df['phoneno_issues'].str.strip()
    df['phoneno_issues']=df['phoneno_issues'].str.replace(r',$','',regex=True)
    df['phoneno_issues']=df['phoneno_issues'].replace('',np.nan)
    validmask=pd.isna(df['phoneno_issues'])
    df.loc[validmask, "cleaned_phoneno"] = df.loc[validmask, "cleaned"]
    df.loc[~validmask, "cleaned_phoneno"] = np.nan
    
    return df


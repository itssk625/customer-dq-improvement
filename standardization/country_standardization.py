import pandas as pd
import pycountry
import numpy as np
from rapidfuzz import process
countries = [
    "india",
    "united states",
    "united kingdom",
    "canada",
    "australia",
    "new zealand",
    "china",
    "japan",
    "south korea",
    "singapore",
    "malaysia",
    "indonesia",
    "thailand",
    "vietnam",
    "philippines",
    "united arab emirates",
    "saudi arabia",
    "qatar",
    "kuwait",
    "oman",
    "bahrain",
    "germany",
    "france",
    "italy",
    "spain",
    "netherlands",
    "switzerland",
    "sweden",
    "norway",
    "denmark",
    "ireland",
    "south africa",
    "egypt",
    "nigeria",
    "kenya",
    "morocco",
    "brazil",
    "argentina",
    "mexico",
    "chile",
    "colombia",
    "peru",
    "russia",
    "turkey",
    "ukraine",
    "poland",
    "pakistan",
    "bangladesh",
    "sri lanka",
    "nepal"
]
iso_codes={
    "india": "IN",
    "united states": "US",
    "united kingdom": "GB",
    "canada": "CA",
    "australia": "AU",
    "new zealand": "NZ",

    "china": "CN",
    "japan": "JP",
    "south korea": "KR",
    "singapore": "SG",
    "malaysia": "MY",
    "indonesia": "ID",
    "thailand": "TH",
    "vietnam": "VN",
    "philippines": "PH",

    "united arab emirates": "AE",
    "saudi arabia": "SA",
    "qatar": "QA",
    "kuwait": "KW",
    "oman": "OM",
    "bahrain": "BH",

    "germany": "DE",
    "france": "FR",
    "italy": "IT",
    "spain": "ES",
    "netherlands": "NL",
    "switzerland": "CH",
    "sweden": "SE",
    "norway": "NO",
    "denmark": "DK",
    "ireland": "IE",

    "south africa": "ZA",
    "egypt": "EG",
    "nigeria": "NG",
    "kenya": "KE",
    "morocco": "MA",

    "brazil": "BR",
    "argentina": "AR",
    "mexico": "MX",
    "chile": "CL",
    "colombia": "CO",
    "peru": "PE",

    "russia": "RU",
    "turkey": "TR",
    "ukraine": "UA",
    "poland": "PL",

    "pakistan": "PK",
    "bangladesh": "BD",
    "sri lanka": "LK",
    "nepal": "NP"
    
}
country_aliases = {
    "republic of india": "india",
    "usa": "united states",
    "us": "united states",
    "america": "united states",
    "uk": "united kingdom",
    "great britain": "united kingdom",
    "britain": "united kingdom",
    "england": "united kingdom",
    "uae": "united arab emirates",
    "emirates": "united arab emirates",
    "korea": "south korea",
    "republic of korea": "south korea",
    "russian federation": "russia",
    "prc": "china",
    "people's republic of china": "china",
    "sultanate of oman": "oman",
    "czechia": "czech republic",
    "holland": "netherlands",
    "brasil": "brazil",
    "sa": "south africa",
    "nz": "new zealand",
    "ksa": "saudi arabia",
    "saudi": "saudi arabia",
    "indai":"india",
    "jpan":"japan",
    "chna":"china","qtr":"qatar","qatr":"qatar","omn":"oman","per":"peru",'pru':"peru",
    "nepl":"nepal"
}


import pandas as pd
'''
df = pd.DataFrame({
    'nationality': [
        'India',
        'indai',
        ' INDIA ',
        'indiaa',

        'USA',
        'US',
        'U.S.A',
        'America',
        'Untied States',

        'UK',
        'England',
        'Great Britain',
        'Untied Kingdom',

        'UAE',
        'Emirates',
        'United Arab Emirats',

        'Canada',
        'Cnada',
        'canadaa',

        'Australia',
        'Australlia',
        'Austraila',

        'Germany',
        'Germnay',

        'France',
        'Frnace',

        'Japan',
        'Jpan',

        'Brazil',
        'Brasil',

        'South Korea',
        'Soth Korea',

        'Russia',
        'Russian Federation',

        'China',
        'Chna',

        '',
        '   ',
        None,

        '123',
        '@@@',
        'Moon',
        'Atlantis',
        'Narnia'
    ]
})
'''

def standardize_country(df):
    df=df.copy()
    df['is_validnationality']=True
    emptymask=(pd.isna(df['country']))|(df['country'].str.strip()=='')
    df.loc[emptymask, 'is_validnationality']=False
    df.loc[emptymask, 'nationality_issue']='No nationality provided'
    
    contains_letters=df['country'].str.contains(r'[a-zA-Z]',regex=True, na=False)
    df.loc[~contains_letters & ~emptymask, 'is_validnationality']=False
    df.loc[~contains_letters & ~emptymask, 'nationality_issue']='Invalid nationality'

    df['cleaned_nationality']=(
        df['country']
        .str.lower()
        .str.replace(r'[^a-z\s\']','',regex=True)
        .str.strip()
    )
    presentmask=df['cleaned_nationality'].isin(countries)
    df.loc[presentmask,'valid_nationality']=df.loc[presentmask,'cleaned_nationality']
    df.loc[~presentmask, 'valid_nationality']=df['cleaned_nationality'].map(country_aliases)
    notmatch=~(df['valid_nationality'].isin(countries))
    for idx in df[notmatch].index:
        match=process.extractOne(
            df.loc[idx, 'cleaned_nationality'],
            countries,
            score_cutoff=80
        )
        if match:
            df.loc[idx, 'valid_nationality']=match[0]
        else:
            df.loc[idx, 'valid_nationality']=np.nan
    mask=pd.isna(df['valid_nationality'])
    df.loc[mask & ~emptymask & contains_letters,'is_validnationality']=False
    df.loc[mask & ~emptymask & contains_letters,'nationality_issue']='Unknown nationality'
    df.loc[~mask, 'iso_code']=df.loc[~mask,'valid_nationality'].map(iso_codes)
    df['valid_nationality']=df['valid_nationality'].str.title()
    return df


#standardize_country(df)

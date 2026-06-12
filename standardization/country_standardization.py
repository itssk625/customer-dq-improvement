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
    "ksa": "saudi arabia"
}
import pandas as pd

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

def standardize_country(df):
    df=df.copy()
    print(countries)
    emptymask=(pd.isna(df['nationality']))|(df['nationality'].str.strip()=='')
    df.loc[emptymask, 'is_validnationality']=False
    df.loc[emptymask, 'nationality_issue']='No nationality provided'
    
    invalid=df['nationality'].str.contains(r'[a-zA-Z]',regex=True, na=False)
    df.loc[~invalid & ~emptymask, 'is_validnationality']=False
    df.loc[~invalid & ~emptymask, 'nationality_issue']='Invalid nationality'

    df['cleaned_nationality']=(
        df['nationality']
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
            score_cutoff=79.9
        )
        if match:
            df.loc[idx, 'valid_nationality']=match[0]
        else:
            df.loc[idx, 'valid_nationality']=np.nan
    df['valid_nationality']=df['valid_nationality'].str.title()
    mask=pd.isna(df['valid_nationality'])
    df.loc[mask & ~emptymask & invalid,'is_validnationality']=False
    df.loc[mask & ~emptymask & invalid,'nationality_issue']='Unknown nationality'
    print(process.extractOne("indai", countries))
    print(df[['nationality', 'cleaned_nationality','valid_nationality','nationality_issue']])
    return df



standardize_country(df)

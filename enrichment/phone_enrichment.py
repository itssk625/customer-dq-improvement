import pandas as pd
import requests
from config import API_KEY

country_codes = {
    "1": "USA",
    "7": "Russia",
    "20": "Egypt",
    "27": "South Africa",
    "30": "Greece",
    "31": "Netherlands",
    "32": "Belgium",
    "33": "France",
    "34": "Spain",
    "39": "Italy",
    "41": "Switzerland",
    "43": "Austria",
    "44": "United Kingdom",
    "45": "Denmark",
    "46": "Sweden",
    "47": "Norway",
    "48": "Poland",
    "49": "Germany",

    "51": "Peru",
    "52": "Mexico",
    "54": "Argentina",
    "55": "Brazil",
    "56": "Chile",
    "57": "Colombia",
    "58": "Venezuela",

    "60": "Malaysia",
    "61": "Australia",
    "62": "Indonesia",
    "63": "Philippines",
    "64": "New Zealand",
    "65": "Singapore",
    "66": "Thailand",

    "81": "Japan",
    "82": "South Korea",
    "84": "Vietnam",
    "86": "China",

    "90": "Turkey",
    "91": "India",
    "92": "Pakistan",
    "93": "Afghanistan",
    "94": "Sri Lanka",
    "95": "Myanmar",
    "98": "Iran",

    "212": "Morocco",
    "213": "Algeria",
    "216": "Tunisia",
    "218": "Libya",

    "220": "Gambia",
    "221": "Senegal",
    "233": "Ghana",
    "234": "Nigeria",
    "254": "Kenya",
    "255": "Tanzania",
    "256": "Uganda",

    "351": "Portugal",
    "352": "Luxembourg",
    "353": "Ireland",
    "354": "Iceland",
    "357": "Cyprus",

    "380": "Ukraine",
    "385": "Croatia",
    "386": "Slovenia",
    "387": "Bosnia and Herzegovina",

    "852": "Hong Kong",
    "853": "Macau",
    "855": "Cambodia",
    "856": "Laos",
    "880": "Bangladesh",
    "886": "Taiwan",

    "960": "Maldives",
    "961": "Lebanon",
    "962": "Jordan",
    "963": "Syria",
    "964": "Iraq",
    "965": "Kuwait",
    "966": "Saudi Arabia",
    "967": "Yemen",
    "968": "Oman",
    "970": "Palestine",
    "971": "United Arab Emirates",
    "972": "Israel",
    "973": "Bahrain",
    "974": "Qatar",
    "975": "Bhutan",
    "976": "Mongolia",
    "977": "Nepal",
}


def get_operator(phone):
    url="http://apilayer.net/api/validate"
    params={
        "access_key": API_KEY,
        "number": phone
    }
    resp=requests.get(url, params=params)
    return resp.json()
def enrich_phones(df):
    df=df.copy()
    df['extracted_country']=df['code'].map(country_codes)    
    cache={}
    for phone in df.loc[df['is_validphoneno'], 'valid_phone'].dropna().unique():
        try:
            cache[phone]=get_operator(phone)
        except Exception as e:
            cache[phone]={}
        
    for idx in df[df['is_validphoneno']].index:
        phone=df.loc[idx, 'valid_phone']
        df.loc[idx, "extracted_operator"]=cache.get(phone, {}).get("carrier")
    
        
    return df


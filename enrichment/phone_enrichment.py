country_codes = {
    "1": "United States",
    "7": "Russia",
    "20": "Egypt",
    "27": "South Africa",
    "30": "Greece",
    "31": "Netherlands",
    "32": "Belgium",
    "33": "France",
    "34": "Spain",
    "39": "Italy",
    "44": "United Kingdom",
    "49": "Germany",
    "52": "Mexico",
    "55": "Brazil",
    "60": "Malaysia",
    "61": "Australia",
    "62": "Indonesia",
    "65": "Singapore",
    "81": "Japan",
    "86": "China",
    "91": "India",
    "92": "Pakistan",
    "93": "Afghanistan",
    "94": "Sri Lanka",
    "95": "Myanmar",
    "966": "Saudi Arabia",
    "971": "United Arab Emirates",
    "974": "Qatar",
    "975": "Bhutan",
    "977": "Nepal"
}

pattern=r'^\+?(\d{1,4})[- ]'
df['extracted_countrycode']=df['phoneno'].str.extract(pattern)
df['extracted_country']=df['extracted_countrycode'].map(country_codes)
import pandas as pd
from rapidfuzz import process
df_typos = pd.DataFrame({
    "expected_country": [
        "india","india","india",
        "united states","united states","united states",
        "united kingdom","united kingdom",
        "canada","canada",
        "australia","australia",
        "germany","germany",
        "france","france",
        "japan","japan",
        "china","china",
        "brazil","brazil",
        "south korea","south korea",
        "united arab emirates","united arab emirates",
        "saudi arabia",
        "russia",
        "new zealand",
        "south africa"
    ],

    "typo": [
        "indai",
        "indiaa",
        "indi",

        "untied states",
        "unites states",
        "unied states",

        "untied kingdom",
        "unites kingdom",

        "cnada",
        "canadaa",

        "australlia",
        "austraila",

        "germnay",
        "germanyy",

        "frnace",
        "francee",

        "jpan",
        "jappan",

        "chna",
        "chiina",

        "brasil",
        "brazill",

        "soth korea",
        "south kora",

        "united arab emirats",
        "unites arab emirates",

        "saudia arabia",

        "russsia",

        "new zealnd",

        "south afrcia"
    ]
})


for _, row in df_typos.iterrows():

    match = process.extractOne(
        row['typo'],
        countries
    )

    print(
        row['typo'],
        "->",
        match[0],
        "| score:",
        round(match[1],2)
    )
import pandas as p
import json
df=p.read_excel('C:/Users/khans/Downloads/dirty_email_cleaning_exercise.xlsx')
df['Normalised Email']=(
    df['Raw Email']
    .astype(str)
    .str.replace('COM','com', regex=False)
    .str.replace('GMAIL','gmail',regex=False)
    .str.replace('OUTLOOK', 'outlook', regex=False)
    .str.replace('YAHOO','yahoo', regex=False)
    .str.replace(r'[#@]+','@',regex=True)
    .str.replace(r'\.+','.', regex=True)
    .str.replace(r'[^a-zA-Z0-9@._]', '', regex=True)
)
mask=(df['Normalised Email'].isnull()| ~df['Normalised Email'].str.match(r'[A-Za-z0-9\._]+@(gmail|yahoo|outlook)\.(com|edu|org)$'))

df.loc[mask,'Normalised Email']='Invalid'
df=df[['Name', 'Raw Email', 'Normalised Email']]
result=df.to_dict(orient='records')
print(json.dumps(result))
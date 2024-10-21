<<<<<<< HEAD

from xata.client import XataClient
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()


client = XataClient(db_url=os.environ.get('REDACTED_DB_URL'), api_key=os.environ.get('XATA_API_KEY'))
=======
REDACTED_DB_URL="https://SirAlph4-s-workspace-2kknuo.eu-central-1.xata.sh/db/my_Database"
WORKSPACE = "SirAlph4-s-workspace-2kknuo"
HTTP_ENDPOINT ="https://SirAlph4-s-workspace-2kknuo.eu-central-1.xata.sh/db/my_Database:main"
XATA_API_KEY="xau_Q0e0PlEuAb6hFxcgMuzOmMFvPleUaqes0"
from xata.client import XataClient
import pandas as pd
import os
client = XataClient(db_url=REDACTED_DB_URL, api_key=XATA_API_KEY)
>>>>>>> c03243f (Initial)
column = [
        "xata_id",
        "CARDINAL",
        "DATE",
        "EVENT",
        "FAC",
        "GPE",
        "ID",
        "LANGUAGE",
        "LAW",
        "LOC",
        "MONEY",
        "NORP",
        "ORDINAL",
        "ORG",
        "PERCENT",
        "PERSON",
        "PRODUCT",
        "QUANTITY",
        "TIME",
        "WORK_OF_ART",
        "article_text",
        "author_name",
        "categories",
        "headline",
        "timestamp",
        "url"
    ]


records = client.data().query("Extracted_Articles", {
    "columns": column,
    "page": {
        "size": 1000
    }
})
df2 = pd.DataFrame.from_dict(records['records'])

i = 0
while records.has_more_results():
    i +=1
    # fetch the next page ...
    records = client.data().query("Extracted_Articles", {
    "columns": column,
    "page": {
        "after": records.get_cursor() # get the next cursor
    }
    })

    new_data = pd.DataFrame.from_dict(records['records'])

    # Append new_data to df2
    df2 = pd.concat([df2, new_data], ignore_index=True)


    if (i == 6):
        break
print(len(df2))
df2.to_csv("Webscrape.csv",index=False, sep=";")
df2.to_excel("Webscrape.xlsx",index=False)
df2.to_json("Webscrape.json",index=False)
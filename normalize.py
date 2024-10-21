import pandas as pd
import ast

# Sample data, assuming it's already loaded into Python from Power BI or a CSV
df = pd.read_csv("Webscrape.csv", sep=";")

# Function to safely evaluate string representations of lists
def safe_eval(x):
    try:
        return ast.literal_eval(x)
    except:
        return [x]

df['ORG'] = df['ORG'].apply(safe_eval)
df['CARDINAL'] = df['CARDINAL'].apply(safe_eval)
df['DATE'] = df['DATE'].apply(safe_eval)
df['EVENT'] = df['EVENT'].apply(safe_eval)
df['FAC'] = df['FAC'].apply(safe_eval)
df['GPE'] = df['GPE'].apply(safe_eval)
df['LANGUAGE'] = df['LANGUAGE'].apply(safe_eval)
df['LAW'] = df['LAW'].apply(safe_eval)
df['LOC'] = df['LOC'].apply(safe_eval)
df['MONEY'] = df['MONEY'].apply(safe_eval)
df['NORP'] = df['NORP'].apply(safe_eval)
df['ORDINAL'] = df['ORDINAL'].apply(safe_eval)
df['PERSON'] = df['PERSON'].apply(safe_eval)
df['PRODUCT'] = df['PRODUCT'].apply(safe_eval)
df['QUANTITY'] = df['QUANTITY'].apply(safe_eval)
df['TIME'] = df['TIME'].apply(safe_eval)
df['WORK_OF_ART'] = df['WORK_OF_ART'].apply(safe_eval)
df['PERCENT'] = df['PERCENT'].apply(safe_eval)
df["WORK_OF_ART"] = df["WORK_OF_ART"].apply(safe_eval)
cardinal_df = pd.DataFrame(columns=["CARDINAL", "ID"])
date_df = pd.DataFrame(columns=["DATE", "ID"])
event_df = pd.DataFrame(columns=["EVENT", "ID"])
fac_df = pd.DataFrame(columns=["FAC", "ID"])
gpe_df = pd.DataFrame(columns=["GPE", "ID"])
language_df = pd.DataFrame(columns=["LANGUAGE", "ID"])
law_df = pd.DataFrame(columns=["LAW", "ID"])
loc_df = pd.DataFrame(columns=["LOC", "ID"])
money_df = pd.DataFrame(columns=["MONEY", "ID"])
norp_df = pd.DataFrame(columns=["NORP", "ID"])
ordinal_df = pd.DataFrame(columns=["ORDINAL", "ID"])
org_df = pd.DataFrame(columns=["ORG", "ID"])
person_df = pd.DataFrame(columns=["PERSON", "ID"])
product_df = pd.DataFrame(columns=["PRODUCT", "ID"])
quantity_df = pd.DataFrame(columns=["QUANTITY", "ID"])
time_df = pd.DataFrame(columns=["TIME", "ID"])
work_of_art_df = pd.DataFrame(columns=["WORK_OF_ART", "ID"])
percent_df = pd.DataFrame(columns=["PERCENT", "ID"])
catagoriez_df = pd.DataFrame(columns=["categories", "ID"])
df["categories"] = df["categories"].apply(safe_eval)
for index, row in df.iterrows():
    ID = row["ID"]
    for org in row["ORG"]:
        org_df.loc[len(org_df)] =  {"ORG": org, "ID": ID}
    for cardinal in row["CARDINAL"]:
        cardinal_df.loc[len(cardinal_df)] =  {"CARDINAL": cardinal, "ID": ID}
    for date in row["DATE"]:
        date_df.loc[len(date_df)] =  {"DATE": date, "ID": ID}
    for event in row["EVENT"]:
        event_df.loc[len(event_df)] =  {"EVENT": event, "ID": ID}
    for fac in row["FAC"]:
        fac_df.loc[len(fac_df)] =  {"FAC": fac, "ID": ID}
    for gpe in row["GPE"]:
        gpe_df.loc[len(gpe_df)] =  {"GPE": gpe, "ID": ID}
    for language in row["LANGUAGE"]:
        language_df.loc[len(language_df)] =  {"LANGUAGE": language, "ID": ID}
    for law in row["LAW"]:
        law_df.loc[len(law_df)] =  {"LAW": law, "ID": ID}
    for loc in row["LOC"]:
        loc_df.loc[len(loc_df)] =  {"LOC": loc, "ID": ID}
    for money in row["MONEY"]:
        money_df.loc[len(money_df)] =  {"MONEY": money, "ID": ID}
    for norp in row["NORP"]:
        norp_df.loc[len(norp_df)] =  {"NORP": norp, "ID": ID}
    for ordinal in row["ORDINAL"]:
        ordinal_df.loc[len(ordinal_df)] =  {"ORDINAL": ordinal, "ID": ID}
    for person in row["PERSON"]:
        person_df.loc[len(person_df)] =  {"PERSON": person, "ID": ID}
    for product in row["PRODUCT"]:
        product_df.loc[len(product_df)] =  {"PRODUCT": product, "ID": ID}
    for quantity in row["QUANTITY"]:
        quantity_df.loc[len(quantity_df)] =  {"QUANTITY": quantity, "ID": ID}
    for time in row["TIME"]:
        time_df.loc[len(time_df)] =  {"TIME": time, "ID": ID}
    for percent in row["PERCENT"]:
        percent_df.loc[len(percent_df)] =  {"PERCENT": percent, "ID": ID}
    # for work_of_art in row["WORK_OF_ART"]:
    #     work_of_art_df.loc[len(work_of_art_df)] =  {"WORK_OF_ART": work_of_art, "ID": ID}
    for catagoriez in row["categories"]:
        catagoriez_df.loc[len(catagoriez_df)] =  {"categories": catagoriez, "ID": ID}

org_df.to_csv("org_normalized.csv", index=False, sep=";")
cardinal_df.to_csv("cardinal_normalized.csv", index=False, sep=";")
date_df.to_csv("date_normalized.csv", index=False, sep=";")
event_df.to_csv("event_normalized.csv", index=False, sep=";")
fac_df.to_csv("fac_normalized.csv", index=False, sep=";")
gpe_df.to_csv("gpe_normalized.csv", index=False, sep=";")
language_df.to_csv("language_normalized.csv", index=False, sep=";")
law_df.to_csv("law_normalized.csv", index=False, sep=";")
loc_df.to_csv("loc_normalized.csv", index=False, sep=";")
money_df.to_csv("money_normalized.csv", index=False, sep=";")
norp_df.to_csv("norp_normalized.csv", index=False, sep=";")
ordinal_df.to_csv("ordinal_normalized.csv", index=False, sep=";")
person_df.to_csv("person_normalized.csv", index=False, sep=";")
product_df.to_csv("product_normalized.csv", index=False, sep=";")
quantity_df.to_csv("quantity_normalized.csv", index=False, sep=";")
time_df.to_csv("time_normalized.csv", index=False, sep=";")      
work_of_art_df.to_csv("work_of_art_normalized.csv", index=False, sep=";")
percent_df.to_csv("percent_normalized.csv", index=False, sep=";")
catagoriez_df.to_csv("catagoriez_normalized.csv", index=False, sep=";")

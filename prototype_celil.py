from xata.client import XataClient
import spacy

# Load the transformer-based NER model
nlp = spacy.load("en_core_web_trf")

REDACTED_DB_URL="https://SirAlph4-s-workspace-2kknuo.eu-central-1.xata.sh/db/my_Database"
WORKSPACE = "SirAlph4-s-workspace-2kknuo"
HTTP_ENDPOINT ="https://SirAlph4-s-workspace-2kknuo.eu-central-1.xata.sh/db/my_Database:main"
XATA_API_KEY="xau_Q0e0PlEuAb6hFxcgMuzOmMFvPleUaqes0"

client = XataClient(db_url=REDACTED_DB_URL, api_key=XATA_API_KEY)

def get_longest_entity(entities, doc):
    """
    Given a list of entity spans and the spaCy doc, return a dictionary with entity labels
    as keys and a list of unique entities as values. For specific labels, include detailed
    referring information when available.
    """
    unique_entities = {}

    def find_referring_entity(ent):
        start = max(0, ent.start - 5)
        end = min(len(doc), ent.end + 5)
        context = doc[start:end].text
        return context.replace(ent.text, "").strip()

    for ent in entities:
        label = ent.label_
        entity_text = ent.text

        if label not in unique_entities:
            unique_entities[label] = set()

        if label in ['CARDINAL', 'PERCENT', 'QUANTITY', 'MONEY', 'TIME', 'DATE', 'ORDINAL']:
            referring_entity = find_referring_entity(ent)
            if referring_entity:
                full_entity = f"{entity_text} ({referring_entity})"
                unique_entities[label].add(full_entity)
            else:
                unique_entities[label].add(entity_text)
        else:
            unique_entities[label].add(entity_text)

    # Convert sets to lists
    for label in unique_entities:
        unique_entities[label] = list(unique_entities[label])

    return unique_entities

def process_document_content(content):
    lines = content.split('\n')
    all_entities = {}

    for line in lines:
        if line.startswith('---------------------------------------'):
            continue

        if ': ' in line:
            label, entities = line.split(': ', 1)
            doc = nlp(entities)
            entities = eval(entities)  # Convert string representation to list

            unique_entities = get_longest_entity(doc.ents, doc)

            for key, value in unique_entities.items():
                if key not in all_entities:
                    all_entities[key] = []
                all_entities[key].extend(value)

    # Remove any remaining duplicates
    for key in all_entities:
        all_entities[key] = list(set(all_entities[key]))

    return all_entities

def extract_unique_entities(text):
    """
    Process the input text and extract unique NER entities, storing all
    entities under the same label and keeping the longest version.
    """
    doc = nlp(text)
    entities = doc.ents  # Extract named entities

    # Remove duplicates and pick longest forms
    unique_entities = get_longest_entity(entities, doc)

    return unique_entities

# Example usage
text = """
In 2023, Apple Inc. sold 1,000,000 iPhones, which is a 20% increase from last year.
Tesla Inc. reported that 500,000 vehicles were delivered last year.
The company's revenue grew by $5 billion.
"""

# Extract entities without duplicates and keep the longest forms
unique_entities = extract_unique_entities(text)

# Output the unique entities
for label, entities in unique_entities.items():
    print(f"{label}: {entities}")

for i in range(1005254, 1005522, 1):
    entity_dict = {
      "PERSON": [],        # People, including fictional.
      "NORP": [],          # Nationalities or religious or political groups.
      "FAC": [],           # Buildings, airports, highways, bridges, etc.
      "ORG": [],           # Companies, agencies, institutions, etc.
      "GPE": [],           # Countries, cities, states.
      "LOC": [],           # Non-GPE locations, mountain ranges, bodies of water.
      "PRODUCT": [],       # Objects, vehicles, foods, etc. (Not services.)
      "EVENT": [],         # Named hurricanes, battles, wars, sports events, etc.
      "WORK_OF_ART": [],   # Titles of books, songs, etc.
      "LAW": [],           # Named documents made into laws.
      "LANGUAGE": [],      # Any named language.
      "DATE": [],          # Absolute or relative dates or periods.
      "TIME": [],          # Times smaller than a day.
      "PERCENT": [],       # Percentage, including ”%“.
      "MONEY": [],         # Monetary values, including unit.
      "QUANTITY": [],      # Measurements, as of weight or distance.
      "ORDINAL": [],       # “first”, “second”, etc.
      "CARDINAL": []       # Numerals that do not fall under another type.
    }
    query_params = {
        "filter": {
            "ID": i
        }
    }
    result = client.data().query("Articles", query_params)
    record_dict = result["records"][0]
    text = record_dict["article_text"]
    del record_dict['xata']
    del record_dict['id']

    unique_entities = extract_unique_entities(text)

    # Loop through the unique entities and extend the corresponding list in the entity_dict
    for label, entity in unique_entities.items():
        entity_dict[label].extend(entity)

    # Merge the entity_dict and record_dict
    input_dict = entity_dict | record_dict
    data = client.records().insert("Extracted_Articles",input_dict)
    print(data)
    print()
    print("---------------------------------------")
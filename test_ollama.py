import logging
import json
from typing import Dict, List, Any, Union
import pandas as pd
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from sysmsg import systemMessage

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_llm(model: str = "qwen2.5:32b") -> ChatOllama:
    """Initialize the ChatOllama model."""
    try:
        return ChatOllama(
            model=model,
            temperature=0.1,  # Low temperature for more focused outputs
            top_k=30,
            top_p=0.5,
            min_p=0.02,
            repeat_penalty=1.2,
            num_predict=512,
            num_ctx=8192,
            mirostat_tau=3.0,
            mirostat_eta=0.1,
        )
    except Exception as e:
        logging.error(f"Error initializing ChatOllama: {e}")
        raise


def create_human_message(article_text, spacy_json):
    
    return f"""
Please analyze the following article text and refine the entity recognition. Also, review and improve upon the entities already extracted by Spacy.

Article Text:
'''{article_text}'''

Entities extracted by Spacy:
'''{spacy_json}'''

Return the refined list of entities as a JSON output only, following the system instructions"""

def extract_entities(llm: ChatOllama, text: str) -> str:
    """Extract entities from the given text."""

    messages = [
        SystemMessage(content=systemMessage),
        HumanMessage(content=text)
    ]
    try:
        # logging.info(f"Invoking the model with the following messages: {messages}")
        response = llm.invoke(messages)
        logging.debug(f"Raw model response: {response.content}")
        return response.content
    except Exception as e:
        logging.error(f"Error extracting entities: {e}")
        raise

def parse_ner_results(response: str) -> Dict[str, Union[List[str], float, int, str]]:
    """Parse the NER results into a structured format."""
    try:
        # Remove the triple backticks and 'json' from the response
        json_content = response.replace('```json', '').replace('```', '').strip()
        entities = json.loads(json_content)
        logging.debug(f"Parsed entities: {entities}")
        return entities
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing NER results: {e}")
        logging.debug(f"Problematic response: {response}")
        return {}

def append_to_dataframe(parsed_results: Dict[str, Union[List[str], float, str]], df: pd.DataFrame, article_id: int) -> pd.DataFrame:
    """Append parsed NER results into an existing DataFrame."""
    data = []
    for category, entities in parsed_results.items():
        if isinstance(entities, list):
            for entity in entities:
                data.append({"ArticleID": article_id, "Category": category, "Entity": entity})
        else:
            # Handle non-list values (like SENTIMENT or SUMMARY)
            data.append({category: str(entities)})
    print(data)
    # Create a new DataFrame and append to the existing one
    new_df= pd.DataFrame(data)
    print(new_df)
    return pd.concat([df, new_df], ignore_index=True)

def save_to_json(df: pd.DataFrame, filename: str = "NER_extracted.json"):
    """Save the DataFrame into a JSON file."""
    try:
        # Convert the DataFrame to JSON format and save it
        df.to_json(filename, orient='records', lines=True)
        logging.info(f"NER results successfully saved to {filename}")
    except Exception as e:
        logging.error(f"Error saving NER results to JSON: {e}")
labels_to_drop = [
    'article_text', 'author_name','categories',
    'headline','id', 'timestamp',
    'url', 'xata', "ID"
]

def main():
    llm = initialize_llm()
    df = pd.DataFrame({})  # Initialize an empty DataFrame
    df_ex = pd.read_csv("Webscrape.csv", nrows=11, sep=";")
    df_ex = df_ex[10:].replace('[]', pd.NA)
    # Iterate through multiple articles in articleText
    for idx, row in df_ex.iterrows():

        article_text = row.at['article_text']
        
        row_edit = row.drop(labels=labels_to_drop).dropna()
        row_dict = row_edit.to_dict()

        # Convert the dictionary to JSON
        spacy_json = json.dumps(row_dict, ensure_ascii=False)

        print(spacy_json)
        text = create_human_message(article_text, spacy_json) 
        response = extract_entities(llm, text)
        parsed_results = parse_ner_results(response)

        print(parsed_results)
        series = pd.Series(parsed_results)
        print(row)
        for key in series.index:
            row[key] = series[key]
        print(row)
        print(row.update(series.to_dict()))
        df = pd.concat([df, row.to_frame().T], ignore_index=True)

    print(df)
    df.to_csv("NER_extracted.csv",sep=";" ,index=False)
    # Save the cumulative results to JSON after processing all articles


if __name__ == "__main__":
    main()
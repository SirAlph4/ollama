import pandas as pd
import ast

# Read the input CSV file
df = pd.read_csv("csv/NER_extracted2.csv", 
                 sep="␟",
                 engine='python',
                 encoding='utf-8')

# Define all entity columns to process
ENTITY_COLUMNS = [
    'ORG', 'EVENT', 'FAC', 'GPE', 'LANGUAGE', 'LAW',
    'LOC', 'NORP', 'PERSON', 'PRODUCT', 'WORK_OF_ART', 'categories',
    'INDUSTRY_SECTOR', 'MARKET_TREND', 'INVESTMENT_TYPE', 
    'TECHNOLOGY_CATEGORY', 'EMPLOYMENT'
]
# Function to convert string representations of lists to actual lists
def safe_eval(x):
    return ast.literal_eval(x) if isinstance(x, str) else [x]

# Convert all entity columns from string representations to lists
for column in ENTITY_COLUMNS:
    df[column] = df[column].apply(safe_eval)

# Create normalized dataframes and lookup tables for each entity type
normalized_dfs = {}
lookup_dfs = {}

for column in ENTITY_COLUMNS:
    # Explode the lists into separate rows
    temp_df = df[['ID', column]].explode(column)
    temp_df = temp_df.drop_duplicates(subset=['ID', column])
    
    # Filter out empty or null values and reset index
    temp_df = temp_df[temp_df[column].notna()]
    temp_df = temp_df.reset_index(drop=True)
    
    # Create lookup table with unique values and their IDs
    unique_values = pd.DataFrame(temp_df[column].unique(), columns=[column])
    unique_values[f'{column}ID'] = range(1, len(unique_values) + 1)
    
    # Create mapping DataFrame
    mapped_df = temp_df.merge(unique_values, on=column, how='left')
    mapped_df = mapped_df[['ID', f'{column}ID']]
    
    # Store both DataFrames
    normalized_dfs[column] = mapped_df
    lookup_dfs[column] = unique_values

# Save all normalized dataframes and lookup tables to CSV files
for entity_type, normalized_df in normalized_dfs.items():
    # Save mapping file (ID to EntityID)
    mapping_filename = f"csv/normalized/{entity_type.lower()}_id_mapping.csv"
    normalized_df.to_csv(mapping_filename, index=False, sep="␟")
    
    # Save lookup file (EntityID to EntityValue)
    lookup_filename = f"csv/normalized/{entity_type.lower()}_lookup.csv"
    lookup_dfs[entity_type].to_csv(lookup_filename, index=False, sep="␟")# Save all normalized dataframes to CSV files



def extract_number_and_description(text):
    if pd.isna(text):
        return pd.NA, pd.NA
    
    text = str(text)
    # Split by opening parenthesis
    parts = text.split('(', 1)
    
    if len(parts) == 2:
        number = parts[0].strip()
        # Remove closing parenthesis from description
        description = parts[1].rstrip(')').strip()
        return number, description
    return text.strip(), ''

S_ENTITY_COLUMNS = [
    'CARDINAL', 'ORDINAL', 'QUANTITY', 'PERCENT', 'MONEY', 'POSITION', 'TIME', "DATE"
]

# Convert all entity columns from string representations to lists
for column in S_ENTITY_COLUMNS:
    df[column] = df[column].apply(safe_eval)

normalized_dfs = {}
for column in S_ENTITY_COLUMNS:
    # Explode the lists into separate rows
    temp_df = df[['ID', column]].explode(column)
    
    # Store the original value before splitting
    temp_df['original_value'] = temp_df[column]
    
    # Extract number and description row by row
    extracted_data = temp_df[column].apply(extract_number_and_description)
    temp_df[f'{column}_value'] = extracted_data.apply(lambda x: x[0])
    temp_df[f'{column}_description'] = extracted_data.apply(lambda x: x[1])
    
    # Drop duplicates after all values are extracted
    temp_df = temp_df.drop_duplicates(subset=['ID', 'original_value'])
    
    # Filter out empty or null values
    temp_df = temp_df[temp_df[column].notna()]
    
    # Reset index
    temp_df = temp_df.reset_index(drop=True)
    
    # Store the normalized dataframe
    normalized_dfs[column] = temp_df

# Save all normalized dataframes to CSV files
for entity_type, normalized_df in normalized_dfs.items():
    output_filename = f"csv/normalized/{entity_type.lower()}_normalized.csv"
    columns_to_save = ['ID', 'original_value', f'{entity_type}_value', f'{entity_type}_description']
    normalized_df[columns_to_save].to_csv(output_filename, index=False, sep="␟", 
                                        header=[entity_type, entity_type, f'{entity_type}_value', f'{entity_type}_description'])

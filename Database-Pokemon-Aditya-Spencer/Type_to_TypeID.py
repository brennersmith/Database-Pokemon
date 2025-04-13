import pandas as pd

# Define the type to TypeID mapping
type_to_id = {
    'Bug': 1, 'Dark': 2, 'Dragon': 3, 'Electric': 4, 'Fairy': 5,
    'Fighting': 6, 'Fire': 7, 'Flying': 8, 'Ghost': 9, 'Grass': 10,
    'Ground': 11, 'Ice': 12, 'Normal': 13, 'Poison': 14, 'Psychic': 15,
    'Rock': 16, 'Steel': 17, 'Water': 18,
}

def convert_types_to_ids(input_csv, output_csv):
    # Read the input Pokémon CSV
    pokemon_df = pd.read_csv(input_csv)

    # Split the 'Types' column (assuming types are comma-separated)
    pokemon_df['Types'] = pokemon_df['Types'].str.split(',\s*')

    # Create a new DataFrame to hold the results
    pokedex_and_types = []

    for _, row in pokemon_df.iterrows():
        pokedex_number = row['Pokedex Number']
        # Convert types to TypeIDs
        type_ids = [type_to_id[type_name] for type_name in row['Types'] if type_name in type_to_id]

        # Create a new row with the Pokedex Number and a string of comma-separated TypeIDs
        type_ids_str = ', '.join(map(str, type_ids))
        pokedex_and_types.append({
            'PokedexNumber': pokedex_number,
            'TypeIDs': type_ids_str
        })

    # Create a DataFrame for the result
    result_df = pd.DataFrame(pokedex_and_types)

    # Save the result to a new CSV
    result_df.to_csv(output_csv, index=False)
    print(f" Types converted to TypeIDs (all on the same line) and saved to {output_csv}")

# Set your input and output file paths
input_file_path = r'C:\Users\adity\Desktop\GrizzHacks\Database-Pokemon\all_pokemon_data.csv'
output_file_path = r'C:\Users\adity\Desktop\GrizzHacks\Database-Pokemon\pokemon_with_types_single_line.csv'

# Run the conversion
convert_types_to_ids(input_file_path, output_file_path)

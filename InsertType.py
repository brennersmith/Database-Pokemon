import psycopg2
import pandas as pd

print("Script started!")

def insert_data_from_excel():
    file_path = r'C:\Users\adity\Desktop\GrizzHacks\Database-Pokemon\all_pokemon_data.csv'
    pokemon_df = pd.read_csv(file_path)


    conn = psycopg2.connect(
        dbname="Pokemon",
        user="postgres",
        password="AdityaKurup",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    type_type = {
    'Bug': 1,
    'Dark': 2,
    'Dragon': 3,
    'Electric': 4,
    'Fairy': 5,
    'Fighting': 6,
    'Fire': 7,
    'Flying': 8,
    'Ghost': 9,
    'Grass': 10,
    'Ground': 11,
    'Ice': 12,
    'Normal': 13,
    'Poison': 14,
    'Psychic': 15,
    'Rock': 16,
    'Steel': 17,
    'Water': 18,
    }
    pokemon_df['Types'] = pokemon_df['Types'].str.split(',\s*')

    pokemon_type_rows = []
    for _, row in pokemon_df.iterrows():
        pokedex_number = row['Pokedex Number']
        types = row['Types']
        if isinstance(types, list):
            for t in types:
                type_id = type_type.get(t)
                if type_id:
                    pokemon_type_rows.append((pokedex_number, type_id))


    # Apply the mapping
    pokemon_df['Types'] = pokemon_df['Types'].map(type_type)
    # Drop rows where generation is still NaN after mapping
    pokemon_df = pokemon_df.dropna(subset=['Types'])
    # Print to verify
    print(pokemon_df[['Types']].head())

    try:
        for _, row in pokemon_df.iterrows():
            print(f"Inserting: {row['Pokedex Number']}, {row['Name']}, {row['Generation']}")
            cursor.execute("""
                INSERT INTO pokemon (pokedexnumber, name, generationid) 
                VALUES (%s, %s, %s)
                ON CONFLICT (pokedexnumber) DO NOTHING;
            """, (row['Pokedex Number'], row['Name'], row['Generation']))

        conn.commit()
        print("Bulk insert completed!")

    except Exception as e:
        print("Error during insert:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
insert_data_from_excel()
import psycopg2
import pandas as pd

def insert_data_from_excel():
    file_path = r'C:\Users\adity\Desktop\GrizzHacks\Database-Pokemon\fixed_pokemon.csv'
    pokemon_df = pd.read_csv(file_path)

    conn = psycopg2.connect(
        dbname="Pokemon",
        user="postgres",
        password="AdityaKurup",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Map the generation strings to integer IDs
    generation_map = {
        'Generation-i': 1,
        'Generation-ii': 2,
        'Generation-iii': 3,
        'Generation-iv': 4,
        'Generation-v': 5,
        'Generation-vi': 6,
        'Generation-vii': 7,
        'Generation-viii': 8,
        'Generation-ix': 9
    }

    # Apply the mapping
    pokemon_df['Generation'] = pokemon_df['Generation'].map(generation_map)

    # Drop rows where generation is still NaN after mapping
    pokemon_df = pokemon_df.dropna(subset=['Generation'])

    try:
        # 1. Insert into Generation table
        for _, row in pokemon_df.iterrows():
            cursor.execute("""
                INSERT INTO Generation (GenerationID, RegionName)
                VALUES (%s, %s)
                ON CONFLICT (GenerationID) DO NOTHING;
            """, (row['Generation'], row['Region']))

        # 2. Insert into Pokemon table
        for _, row in pokemon_df.iterrows():
            print(f"Inserting: #{row['Pokedex Number']}, Name={row['Name']}, Gen={row['Generation']}")

            # Insert PokedexNumber, Name, GenerationID, and Evolution
            cursor.execute("""
                INSERT INTO pokemon (pokedexnumber, name, generationid, evolution)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (pokedexnumber) DO NOTHING;
            """, (
                row['Pokedex Number'],
                row['Name'],
                row['Generation'],
                # We only store "Evolution" from CSV; ignoring "Previous Evolution"
                row['Evolution_to']
            ))

        conn.commit()
        print("Bulk insert completed!")

    except Exception as e:
        print("Error during insert:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("Script started!")
    insert_data_from_excel()

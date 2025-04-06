import psycopg2
import pandas as pd
import os

def insert_data_from_excel():
    # Read data from CSV
    file_path = r'C:\Users\adity\Desktop\GrizzHacks\Database-Pokemon\all_pokemon_data.csv'
    pokemon_df = pd.read_csv(file_path)
    print("Columns:", pokemon_df.columns.tolist())
    print(pokemon_df.head(10))
    
    # Ensure correct data types
    pokemon_df["Generation"] = pd.to_numeric(pokemon_df["Generation"], errors='coerce')
    pokemon_df = pokemon_df.dropna(subset=["Generation"])
    pokemon_df["Generation"] = pokemon_df["Generation"].astype(int)


    
    # Ensure that "Types" is properly formatted (if it's a list, it needs parsing)
    if "TypeID" in pokemon_df.columns:
        pokemon_df["TypeID"] = pokemon_df["TypeID"].astype(int)

    print(pokemon_df["Generation"])
    
    conn = None
    cursor = None

    try:
        # Connect to PostgreSQL database (use environment variables instead of hardcoded password)
        conn = psycopg2.connect(
            dbname="Pokemon",
            user="postgres",
            password="AdityaKurup",  # Store password in an environment variable
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Insert into pokemon table
        for _, row in pokemon_df.iterrows():
            cursor.execute("""
                INSERT INTO pokemon (PokedexNumber, name, ) VALUES (%s, %s)
                ON CONFLICT (PokedexNumber) DO NOTHING;
            """, (row['pokedexnumber'], row['name'] ))
        
        # Insert into pokemon_type table
        for _, row in pokemon_df.iterrows():
            cursor.execute("""
                INSERT INTO pokemon_type(PokedexNumber, TypeID) VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
            """, (row['PokedexNumber'], row['TypeID']))
        
        # Insert into type table
        for _, row in pokemon_df.iterrows():
            cursor.execute("""
                INSERT INTO type(TypeID, TypeName) VALUES (%s, %s)
                ON CONFLICT (TypeID) DO NOTHING;
            """, (row['TypeID'], row['TypeName']))
        
        # Insert into Generation table
        for _, row in pokemon_df.iterrows():
            cursor.execute("""
                INSERT INTO Generation(GenerationID, RegionName) VALUES (%s, %s)
                ON CONFLICT (GenerationID) DO NOTHING;
            """, (row['Generation'], row['RegionName']))
        
        conn.commit()
        print("Data inserted successfully")

    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Call the function
insert_data_from_excel()

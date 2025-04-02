import psycopg2
import pandas as pd

def insert_data_from_excel():
    # Read data from csv files
    pokemon_df = pd.read_csv(r'Database-Pokemon/all_pokemon_data.csv', engine='openpyxl')

    pokemon_df["Generation"] = pokemon_df["Generation"].astype(int)
    pokemon_df["Types"] = pokemon_df["Types"].astype(int)
    print(pokemon_df["Types"])
    print(pokemon_df["Generation"])
    
    conn = None  # Initialize connection variable
    cursor = None  # Initialize cursor variable

    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname="HW5",
            user="postgres",
            password="AdityaKurup",  # Replace with actual password
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        
        for _, row in pokemon_df.iterrows():
            cursor.execute("""
            INSERT INTO pokemon (PokedexNumber, name, GenerationID) VALUES (%s, %s, %s);
            """, (row['PokedexNumber'], row['name'], row['Generation']))
        
        for _, row in pokemon_df.iterrows():
            cursor.execute("""
            INSERT INTO  pokemon_type(PokedexNumber, name, GenerationID) VALUES (%s, %s, %s);
            """, (row['PokedexNumber'], row['name'], row['Generation']))
        

        # Commit changes
        conn.commit()
        print("Data inserted successfully")

    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()  # Rollback changes only if connection exists

    finally:
        if cursor:
            cursor.close()  # Close cursor only if it was created
        if conn:
            conn.close()  # Close connection only if it was established

# Call the function to insert data from Excel files
insert_data_from_excel()

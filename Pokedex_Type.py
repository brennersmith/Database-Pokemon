import psycopg2
import pandas as pd

print("Script started!")

def insert_data_from_excel():
    file_path = r'C:\Users\Spencer Roeren\Downloads\Code - Copy\Database-Pokemon\pokemon_with_types_single_line.csv'
    pokemon_df = pd.read_csv(file_path)

    conn = psycopg2.connect(
        dbname="Pokemon",
        user="postgres",
        password="2905",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    
    try:
        for _, row in pokemon_df.iterrows():
            # Split the comma-separated TypeIDs into a list of integers
            type_ids = row['TypeIDs'].split(', ')
            for type_id in type_ids:
                cursor.execute("""
                    INSERT INTO pokemon_type(PokedexNumber, TypeID) 
                    VALUES (%s, %s)
                    ON CONFLICT (PokedexNumber, TypeID) DO NOTHING;
                """, (row['PokedexNumber'], int(type_id))) 

        conn.commit()
        print("Bulk insert completed!")

    except Exception as e:
        print("Error during insert:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

insert_data_from_excel()

import psycopg2
import json
import requests

def create_table():
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname='Pokemon',
        user='postgres',
        password='AdityaKurup',
        host='localhost',
        port='5432'
    )

    cursor = conn.cursor()

    # 1) Drop tables if they exist (in case of an old schema)
    drop_pokemon_type_table = "DROP TABLE IF EXISTS pokemon_type CASCADE;"
    drop_search_table = "DROP TABLE IF EXISTS search CASCADE;"
    drop_pokemon_table = "DROP TABLE IF EXISTS pokemon CASCADE;"
    drop_generation_table = "DROP TABLE IF EXISTS generation CASCADE;"
    drop_type_table = "DROP TABLE IF EXISTS type CASCADE;"

    # 2) Create fresh tables
    create_generation_table = """
        CREATE TABLE IF NOT EXISTS Generation(
            GenerationID SERIAL PRIMARY KEY,
            RegionName VARCHAR(50)
        );
    """

    create_pokemon_table = """
        CREATE TABLE IF NOT EXISTS pokemon(
            PokedexNumber SERIAL PRIMARY KEY,
            name VARCHAR(50),
            GenerationID INTEGER,
            evolution VARCHAR(1000),  -- evolution column
            FOREIGN KEY (GenerationID) REFERENCES Generation(GenerationID) ON DELETE SET NULL
        );
    """

    create_type_table = """
        CREATE TABLE IF NOT EXISTS Type(
            TypeID SERIAL PRIMARY KEY,
            TypeName VARCHAR(50)
        );
    """

    create_search_table = """
        CREATE TABLE IF NOT EXISTS Search(
            SearchID SERIAL PRIMARY KEY,
            searchPokedexID INTEGER
        );
    """

    create_pokemon_type_table = """
        CREATE TABLE IF NOT EXISTS pokemon_type(
            PokedexNumber INTEGER,
            TypeID INTEGER,
            PRIMARY KEY (PokedexNumber, TypeID),
            FOREIGN KEY (PokedexNumber) REFERENCES pokemon(PokedexNumber) ON DELETE CASCADE,
            FOREIGN KEY (TypeID) REFERENCES type(TypeID) ON DELETE CASCADE
        );
    """

    try:
        # Drop any existing tables to avoid conflicts
        cursor.execute(drop_pokemon_type_table)
        cursor.execute(drop_search_table)
        cursor.execute(drop_pokemon_table)
        cursor.execute(drop_generation_table)
        cursor.execute(drop_type_table)

        # Now create fresh tables
        cursor.execute(create_generation_table)
        cursor.execute(create_pokemon_table)
        cursor.execute(create_type_table)
        cursor.execute(create_search_table)
        cursor.execute(create_pokemon_type_table)

        conn.commit()
        print("Tables dropped (if existed) and recreated successfully")

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_table()

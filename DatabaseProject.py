import psycopg2
import json

def create_table():
    #Connect to postgreSQL
    
    conn = psycopg2.connect(
        dbname='Pokemon',
        user='postgres',
        password='AdityaKurup',
        host='localhost',
        port='5432'
    )

    #Creates the cursor
    cursor=conn.cursor()
    #SQL tables
    create_Pokemon_table="""
        CREATE TABLE IF NOT EXISTS pokemon(
            PokedexNumber SERIAL PRIMARY KEY,
            name VARCHAR(50),
            GenerationID INTEGER
    );
    """
    
    create_Type_table="""
        CREATE TABLE IF NOT EXISTS Type(
            TypeID SERIAL PRIMARY KEY,
            TypeName VARCHAR(50)
        );
    """
    create_Generation_table="""
        CREATE TABLE IF NOT EXISTS Generation(
            GenerationID SERIAL PRIMARY KEY,
            RegionName VARCHAR(50)
        );
    """
    create_Search_table="""
        CREATE TABLE IF NOT EXISTS Search(
            SearchID SERIAL PRIMARY KEY,
            searchPokedexID INTEGER  
        );
    """

    try:
        # Execute SQL statements to create tables
        cursor.execute(create_Pokemon_table)
        cursor.execute(create_Type_table)
        cursor.execute(create_Generation_table)
        cursor.execute(create_Search_table)

    
        #Commit changes to the database
        conn.commit()
        print("Tables created successfully")
    
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()
    
create_table()
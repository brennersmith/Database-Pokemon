import psycopg2
import pandas as pd

def insert_data_from_excel():
    # Read data from Excel files
    pokemon_df = pd.read_excel(r'Database-Pokemon/all_pokemon_data.csv', engine='openpyxl')

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
            INSERT INTO                
            
            """)
        

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

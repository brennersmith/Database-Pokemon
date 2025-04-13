import psycopg2

def insert_type_data():
    # Define your type mapping (TypeName → TypeID)
    types = {
        1: 'Bug', 2: 'Dark', 3: 'Dragon', 4: 'Electric',
        5: 'Fairy', 6: 'Fighting', 7: 'Fire', 8: 'Flying',
        9: 'Ghost', 10: 'Grass', 11: 'Ground', 12: 'Ice',
        13: 'Normal', 14: 'Poison', 15: 'Psychic', 16: 'Rock',
        17: 'Steel', 18: 'Water'
    }

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname="Pokemon",
            user="postgres",
            password="AdityaKurup",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        for type_id, type_name in types.items():
            cursor.execute("""
                INSERT INTO Type (TypeID, TypeName)
                VALUES (%s, %s)
                ON CONFLICT (TypeID) DO NOTHING;
            """, (type_id, type_name))

        conn.commit()
        print("Type table created and data inserted.")

    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Run it
insert_type_data()
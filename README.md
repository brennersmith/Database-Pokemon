# Database-Pokemon
Instructions on how to run our code :)
All the necessary CSVs should already be a part of the GitHub, but if you don't have them don't worry we have the scripts inside the repo that makes 
them :)
For all_pokemon_data.csv ---> Run PokeAPI_to_Excel.py
For pokemon_with_types.csv ---> Run Type_to_TypeID.py
For fixed_pokemon.csv ---> Run fixevo.py
The prerequisites to using this repo would be to have a working PG admin account because we did use a PostgreSQL database and to have a database in 
PG admin named Pokemon
Please have PG admin open throughout the entire process

Step 1: Run the Database_project.py file with PGadmin open and change the file to have your PG admin password and username in file (and if you want to you can change the database name to whatever you want).

Step 2: Please make sure to change your username and password for PostgreSQL. Run the PokemonTable.py file to insert information into the Generation and Pokemon Table. 

Step 3: Please make sure to change your username and password for PostgreSQL. Run the TypeID.py file, to insert the information into the type table

Step 4: Please make sure to change your username and password for PostgreSQL. Run the Pokedex_Type.py file to insert the Pokedex_Type file.

Step 5: Run Pokemon_GUI.py file to open our Pokedex.

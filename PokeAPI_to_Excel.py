import requests
import pandas as pd

# Function to get all Pokémon names from PokeAPI
def get_all_pokemon():
    url = "https://pokeapi.co/api/v2/pokemon?limit=10000"  # Get all Pokémon
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        pokemon_list = [pokemon["name"] for pokemon in data["results"]]
        return pokemon_list
    else:
        print("Failed to fetch Pokémon list.")
        return []

# Function to fetch individual Pokémon details
def fetch_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        pokedex_number = data["id"]
        name = data["name"].capitalize()
        types = [type_info["type"]["name"].capitalize() for type_info in data["types"]]
        type_str = ", ".join(types)

        # Get species data to fetch Generation, Evolution, and Region
        species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokedex_number}"
        species_response = requests.get(species_url)

        if species_response.status_code == 200:
            species_data = species_response.json()
            
            # Generation
            generation_id = species_data["generation"]["name"].capitalize()

            # Region (if exists)
            region = species_data.get("region", None)
            region_name = region["name"].capitalize() if region else "Unknown"
            
            # Evolution Chain
            evolution_chain_url = species_data["evolution_chain"]["url"]
            evolution_response = requests.get(evolution_chain_url)

            if evolution_response.status_code == 200:
                evolution_data = evolution_response.json()
                evolutions = get_evolution_names(evolution_data["chain"])
                previous_evolution = evolutions[0] if len(evolutions) > 1 else "None"
                evolution_str = ", ".join(evolutions[1:]) if len(evolutions) > 1 else "None"
            else:
                previous_evolution = "None"
                evolution_str = "None"
        else:
            generation_id = None
            region_name = None
            previous_evolution = None
            evolution_str = None
        
        return {
            "Pokedex Number": pokedex_number,
            "Name": name,
            "Types": type_str,
            "Generation": generation_id,
            "Region": region_name,
            "Previous Evolution": previous_evolution,
            "Evolution": evolution_str
        }
    else:
        print(f"Error fetching data for {pokemon_name}: HTTP {response.status_code}")
        return None

# Function to extract evolution names from the chain data
def get_evolution_names(chain_data):
    names = []
    current_chain = chain_data
    while current_chain:
        names.append(current_chain["species"]["name"].capitalize())
        if current_chain["evolves_to"]:
            current_chain = current_chain["evolves_to"][0]
        else:
            break
    return names

# Get Pokémon names and fetch their data
pokemon_names = get_all_pokemon()

pokemon_data = [fetch_pokemon_data(pokemon) for pokemon in pokemon_names]
pokemon_data = [p for p in pokemon_data if p is not None]

# Create a DataFrame and save to CSV
df = pd.DataFrame(pokemon_data)

df.to_csv("all_pokemon_data.csv", index=False)
print("Data saved to all_pokemon_data.csv")

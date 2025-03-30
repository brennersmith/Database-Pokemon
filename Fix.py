import pandas as pd

# Define the mapping of Generation to Region
generation_to_region = {
    "Generation-i": "Kanto",
    "Generation-ii": "Johto",
    "Generation-iii": "Hoenn",
    "Generation-iv": "Sinnoh",
    "Generation-v": "Unova",
    "Generation-vi": "Kalos",
    "Generation-vii": "Alola",
    "Generation-viii": "Galar",
    "Generation-ix": "Paldea"
}

# Load the CSV file
csv_file = "all_pokemon_data.csv"  # Replace with your actual filename
df = pd.read_csv(csv_file)

# Update the Region column based on the Generation column
df["Region"] = df["Generation"].map(generation_to_region).fillna("Unknown")

# Save the updated CSV file
df.to_csv("all_pokemon_data.csv", index=False)

print("CSV file has been updated successfully.")
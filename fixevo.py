import csv

# Read and collect evolution chains
pokemon_data = []
name_to_chain = {}

with open('fixed_pokemon.csv', 'r') as infile:
    reader = csv.reader(infile)
    for row in reader:
        pokemon_data.append(row)
        name = row[1]
        full_chain = row[-2].split(',') + row[-1].split(',')
        full_chain = [p.strip() for p in full_chain if p.strip()]
        # Ensure the full chain has no duplicates
        full_chain = list(dict.fromkeys(full_chain))
        if name not in full_chain:
            full_chain.append(name)
        name_to_chain[name] = full_chain

# Rebuild evolution links
fixed_rows = []
for row in pokemon_data:
    name = row[1]
    chain = name_to_chain.get(name, [])
    if name in chain:
        i = chain.index(name)
        evolves_from = chain[i - 1] if i > 0 else ''
        evolves_to = chain[i + 1] if i < len(chain) - 1 else ''
    else:
        evolves_from = ''
        evolves_to = ''
    
    # Replace the two last columns
    row[-2] = evolves_from
    row[-1] = evolves_to
    fixed_rows.append(row)

# Write cleaned data
with open('fixed_pokemon12.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(fixed_rows)
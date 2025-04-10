import tkinter as tk
from tkinter import ttk  # For Combobox/OptionMenu if you prefer
import psycopg2
import pandas as pd
import os

class PokedexGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pokedex")
        self.geometry("800x500")
        self.configure(background="crimson")

        # Make the GUI responsive in both directions
        self.rowconfigure([0, 1, 2, 3], weight=1)  # 4 rows
        self.columnconfigure([0, 1, 2], weight=1) # 3 columns

        # Try loading data from CSV (you can adapt to load from PostgreSQL instead)
        self.pokemon_data = self.load_data_from_csv("all_pokemon_data.csv")

        # Create a list of Pokémon names for the search box
        self.all_names = list(self.pokemon_data["Name"]) if not self.pokemon_data.empty else []
        
        # Track whichever Pokémon is currently displayed (start with index=0)
        self.current_index = 0

        # Build out the frames/labels as in your layout
        self.create_widgets()
        
        # Initialize the UI with the 1st Pokémon if data is available
        if self.all_names:
            self.update_ui_for_pokemon(self.all_names[self.current_index])

    def load_data_from_csv(self, csv_path):
        """
        Loads all_pokemon_data.csv into a pandas DataFrame.
        Adjust as needed to fetch from your PostgreSQL database instead.
        """
        if os.path.isfile(csv_path):
            try:
                df = pd.read_csv(csv_path)
                return df
            except Exception as e:
                print(f"Error loading CSV: {e}")
                return pd.DataFrame()
        else:
            print(f"CSV file '{csv_path}' not found.")
            return pd.DataFrame()

    def create_widgets(self):
        """
        Constructs frames and labels as specified in your original layout.
        Replaces the 'Species' and 'Catch Rate' labels with 'Previous Evolution' 
        and 'Next Evolution'.
        """
        ### Name Frame
        self.name_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=4)
        self.name_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.name_label = tk.Label(self.name_frame, text="Pokemon Name Here", font=("Futura", 16))
        self.name_label.pack()

        ### Picture Frame
        self.picture_frame = tk.Frame(self, relief=tk.SUNKEN, borderwidth=2)
        self.picture_frame.grid(row=1, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)
        self.picture_label = tk.Label(self.picture_frame, text="Pokemon Picture Here", font=("Futura", 16))
        self.picture_label.pack()

        ### Type Frame
        self.type_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=2)
        self.type_frame.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.type1label = tk.Label(self.type_frame, text="Type 1 Here", font=("Futura", 12))
        self.type1label.grid(row=0, column=0, padx=5)
        self.type2label = tk.Label(self.type_frame, text="Type 2 Here", font=("Futura", 12))
        self.type2label.grid(row=0, column=1, padx=5)

        ### Search Frame
        self.search_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=2)
        self.search_frame.grid(row=0, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

        # Make it responsive
        self.search_frame.columnconfigure([0, 1, 2, 3], weight=1)

        # Left/Right Arrows (could be buttons)
        self.left_arrow_label = tk.Label(self.search_frame, text="Left Arrow", font=("Futura", 16))
        self.left_arrow_label.grid(row=0, column=0, padx=5)

        # A dropdown menu or Combobox in the center
        self.search_var = tk.StringVar()
        self.search_box = ttk.Combobox(
            self.search_frame,
            textvariable=self.search_var,
            values=self.all_names,  # list of Pokémon names
            state="readonly"        # user can only pick from the list
        )
        self.search_box.grid(row=0, column=1, columnspan=2, padx=5)
        self.search_box.bind("<<ComboboxSelected>>", self.on_search_select)

        self.right_arrow_label = tk.Label(self.search_frame, text="Right Arrow", font=("Futura", 16))
        self.right_arrow_label.grid(row=0, column=3, padx=5)

        ### Info Frame
        self.info_frame = tk.Frame(self, relief=tk.SUNKEN, borderwidth=4)
        self.info_frame.grid(row=1, column=1, rowspan=3, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Make the info frame more flexible
        self.info_frame.rowconfigure([0, 1, 2], weight=1)
        self.info_frame.columnconfigure([0, 1], weight=1)

        # Various Information
        self.pokedex_entry = tk.Label(self.info_frame, text="Pokedex Entry", font=("Futura", 16))
        self.pokedex_entry.grid(row=0, column=0, columnspan=2, pady=5)

        self.height_entry = tk.Label(self.info_frame, text="Height", font=("Futura", 16))
        self.height_entry.grid(row=1, column=0, padx=5, pady=5)

        self.weight_entry = tk.Label(self.info_frame, text="Weight", font=("Futura", 16))
        self.weight_entry.grid(row=1, column=1, padx=5, pady=5)

        # Replacing 'Species' and 'Catch Rate' with 'Previous Evolution' and 'Next Evolution'
        self.prev_evo_label = tk.Label(self.info_frame, text="Previous Evolution", font=("Futura", 16))
        self.prev_evo_label.grid(row=2, column=0, padx=5, pady=5)

        self.next_evo_label = tk.Label(self.info_frame, text="Next Evolution", font=("Futura", 16))
        self.next_evo_label.grid(row=2, column=1, padx=5, pady=5)

    def on_search_select(self, event):
        """
        Fired when the user picks a Pokémon from the Combobox.
        Update the UI for that Pokémon.
        """
        selected_name = self.search_var.get()  # e.g. "Pikachu"
        self.update_ui_for_pokemon(selected_name)

    def update_ui_for_pokemon(self, pokemon_name):
        """
        Given a Pokémon name (e.g. "Pikachu"), look up its row in
        self.pokemon_data and fill in the labels accordingly.
        """
        if self.pokemon_data.empty:
            return  # no data

        # Find the row in the DataFrame
        row = self.pokemon_data.loc[self.pokemon_data["Name"] == pokemon_name]
        if row.empty:
            return  # no match

        # For safety, grab the first match
        row = row.iloc[0]

        # Update Name
        self.name_label.config(text=row.get("Name", "???"))

        # Picture placeholder (you could load an actual image if you have one)
        self.picture_label.config(text=f"{row.get('Name', '')} Picture")

        # If "Types" is in your CSV (e.g. "Fire, Flying"), parse it
        types_str = row.get("Types", "")
        split_types = types_str.split(",") if isinstance(types_str, str) else []
        if len(split_types) >= 1:
            self.type1label.config(text=split_types[0].strip())
        else:
            self.type1label.config(text="")

        if len(split_types) >= 2:
            self.type2label.config(text=split_types[1].strip())
        else:
            self.type2label.config(text="")

        # Pokedex entry
        self.pokedex_entry.config(text=f"Pokedex # {row.get('Pokedex Number', '')}")

        # Height, Weight – placeholders unless your CSV actually has these columns
        # For demonstration, let's fill them with region/generation info if columns don't exist
        gen = row.get("Generation", "Unknown")
        region = row.get("Region", "Unknown")

        self.height_entry.config(text=f"Gen: {gen}")
        self.weight_entry.config(text=f"Region: {region}")

        # Previous Evolution & Next Evolution
        previous_evo = row.get("Previous Evolution", "None")
        next_evo = row.get("Evolution", "None")

        self.prev_evo_label.config(text=f"Previous Evolution: {previous_evo}")
        self.next_evo_label.config(text=f"Next Evolution: {next_evo}")

        # Optionally set the Combobox selection to match
        self.search_var.set(pokemon_name)

def main():
    app = PokedexGUI()
    app.mainloop()

if __name__ == "__main__":
    main()

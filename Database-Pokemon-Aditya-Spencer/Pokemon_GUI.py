import tkinter as tk
from tkinter import ttk
import psycopg2
import pandas as pd
import os
import requests
from PIL import Image, ImageTk
import io
import re

class PokedexGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pokedex")
        self.geometry("800x500")
        self.configure(background="crimson")

        # Keep a reference to the last fetched sprite so it doesn't get garbage-collected
        self.current_sprite = None

        # Make the GUI responsive in both directions
        self.rowconfigure([0, 1, 2, 3], weight=1)  # 4 rows
        self.columnconfigure([0, 1, 2], weight=1) # 3 columns

        # Load data from the PostgreSQL database
        self.pokemon_data = self.load_data_from_db()

        # Create a list of Pokémon names for the search box
        if not self.pokemon_data.empty:
            self.all_names = list(self.pokemon_data["name"])
        else:
            self.all_names = []
        
        # Track whichever Pokémon is currently displayed (start with index=0)
        self.current_index = 0

        # Build out the frames/labels
        self.create_widgets()
        
        # Initialize the UI with the 1st Pokémon if data is available
        if self.all_names:
            self.update_ui_for_pokemon(self.all_names[self.current_index])

    def load_data_from_db(self):
        """
        Connect to PostgreSQL and returns a DataFrame containing
        Pokémon info joined with generation, type info, and 'Evolution' field.
        """
        try:
            conn = psycopg2.connect(
                dbname="Pokemon",
                user="postgres",
                password="1018",
                host="localhost",
                port="5432"
            )

            query = """
                SELECT
                    p.pokedexnumber,
                    p.name,
                    p.generationid,
                    g.regionname AS region,
                    COALESCE(string_agg(t.typename, ',' ORDER BY t.typename), '') AS types,
                    p.evolution AS "Evolution"
                FROM pokemon p
                LEFT JOIN generation g
                       ON p.generationid = g.generationid
                LEFT JOIN pokemon_type pt
                       ON p.pokedexnumber = pt.pokedexnumber
                LEFT JOIN type t
                       ON pt.typeid = t.typeid
                GROUP BY p.pokedexnumber, p.name, p.generationid, g.regionname, p.evolution
                ORDER BY p.pokedexnumber;
            """

            df = pd.read_sql(query, conn)
            return df
        
        except Exception as e:
            print(f"Error loading data from PostgreSQL: {e}")
            return pd.DataFrame()
        finally:
            if 'conn' in locals():
                conn.close()

    def create_widgets(self):
        """
        Same layout, but the Combobox is made searchable by:
        - state="normal"
        - binding <KeyRelease> for partial match filtering
        """
        # Fonts (change as you see fit)
        title_font = ("Comic Sans MS", 20, "bold")
        medium_font = ("Comic Sans MS", 16)
        small_font = ("Comic Sans MS", 12)

        ### Name Frame
        self.name_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=4)
        self.name_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.name_label = tk.Label(self.name_frame, text="Pokemon Name Here", font=title_font)
        self.name_label.pack()

        ### Picture Frame
        self.picture_frame = tk.Frame(self, relief=tk.SUNKEN, borderwidth=2)
        self.picture_frame.grid(row=1, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)
        self.picture_label = tk.Label(self.picture_frame, text="Pokemon Picture Here", font=medium_font)
        self.picture_label.pack()

        ### Type Frame
        self.type_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=2)
        self.type_frame.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.type1label = tk.Label(self.type_frame, text="Type 1 Here", font=small_font)
        self.type1label.grid(row=0, column=0, padx=5)
        self.type2label = tk.Label(self.type_frame, text="Type 2 Here", font=small_font)
        self.type2label.grid(row=0, column=1, padx=5)

        ### Search Frame
        self.search_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=2)
        self.search_frame.grid(row=0, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
        self.search_frame.columnconfigure([0, 1, 2, 3], weight=1)

        # Left Arrow button
        self.left_arrow_button = tk.Button(
            self.search_frame,
            text="←",    
            font=medium_font,
            command=self.show_previous_pokemon
        )
        self.left_arrow_button.grid(row=0, column=0, padx=5)

        # A "searchable" Combobox in the center
        self.search_var = tk.StringVar()
        self.search_box = ttk.Combobox(
            self.search_frame,
            textvariable=self.search_var,
            values=self.all_names,
            font=medium_font,
            state="normal"  # user can type
        )
        self.search_box.grid(row=0, column=1, columnspan=2, padx=5)

        # Bind events:
        self.search_box.bind("<<ComboboxSelected>>", self.on_search_select)
        self.search_box.bind("<KeyRelease>", self.on_search_key_release)

        # Right Arrow button
        self.right_arrow_button = tk.Button(
            self.search_frame,
            text="→",
            font=medium_font,
            command=self.show_next_pokemon
        )
        self.right_arrow_button.grid(row=0, column=3, padx=5)

        ### Info Frame
        self.info_frame = tk.Frame(self, relief=tk.SUNKEN, borderwidth=4)
        self.info_frame.grid(row=1, column=1, rowspan=3, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.info_frame.rowconfigure([0, 1, 2], weight=1)
        self.info_frame.columnconfigure([0, 1], weight=1)

        self.pokedex_entry = tk.Label(self.info_frame, text="Pokedex Entry", font=medium_font)
        self.pokedex_entry.grid(row=0, column=0, columnspan=2, pady=5)

        self.height_entry = tk.Label(self.info_frame, text="Height", font=medium_font)
        self.height_entry.grid(row=1, column=0, padx=5, pady=5)

        self.weight_entry = tk.Label(self.info_frame, text="Weight", font=medium_font)
        self.weight_entry.grid(row=1, column=1, padx=5, pady=5)

        # Single 'Evolution' label
        self.evolution_label = tk.Label(self.info_frame, text="Evolution", font=medium_font)
        self.evolution_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def on_search_select(self, event):
        """User picks a Pokémon from the filtered list or hits Enter on a matched item."""
        selected_name = self.search_var.get()
        self.update_ui_for_pokemon(selected_name)

    def on_search_key_release(self, event):
        """
        As the user types, filter self.all_names by partial match
        and update the Combobox values. Then re-set typed text
        so it doesn't auto-select or overwrite the user's input.
        """
        # Save what the user typed
        typed_text = self.search_var.get()

        # Filter the full list
        if typed_text == "":
            # If user cleared everything, show the full list again
            filtered = self.all_names
        else:
            # Partial-match filter (case-insensitive)
            typed_text_lower = typed_text.lower()
            filtered = [name for name in self.all_names if typed_text_lower in name.lower()]

        # Update the Combobox with the filtered list
        self.search_box["values"] = filtered

        # Restore the typed text so it doesn't get overwritten
        self.search_var.set(typed_text)

        # Move the insertion cursor to the end, so user keeps typing
        self.search_box.icursor(tk.END)

        # Optionally open the drop-down to show matches immediately
        self.search_box.event_generate("<Down>")

    def show_previous_pokemon(self):
        """ Decrement the current index and update the UI. """
        if not self.all_names:
            return
        self.current_index = (self.current_index - 1) % len(self.all_names)
        pokemon_name = self.all_names[self.current_index]
        self.update_ui_for_pokemon(pokemon_name)

    def show_next_pokemon(self):
        """ Increment the current index and update the UI. """
        if not self.all_names:
            return
        self.current_index = (self.current_index + 1) % len(self.all_names)
        pokemon_name = self.all_names[self.current_index]
        self.update_ui_for_pokemon(pokemon_name)

    def update_ui_for_pokemon(self, pokemon_name):
        """Look up its row in self.pokemon_data and fill in the labels accordingly."""
        if self.pokemon_data.empty:
            return

        row = self.pokemon_data.loc[self.pokemon_data["name"] == pokemon_name]
        if row.empty:
            return

        row = row.iloc[0]

        # Name
        self.name_label.config(text=row.get("name", "???"))
        # Picture placeholder
        self.picture_label.config(text=f"{row.get('name', '')} Picture")

        # Types
        types_str = row.get("types", "")
        split_types = types_str.split(",") if isinstance(types_str, str) else []
        self.type1label.config(text=split_types[0].strip() if len(split_types) >= 1 else "Type 1")
        self.type2label.config(text=split_types[1].strip() if len(split_types) >= 2 else "Type 2")

        # Pokedex entry
        self.pokedex_entry.config(text=f"Pokedex # {row.get('pokedexnumber', '')}")

        # Height, Weight
        generation_id = row.get("generationid", "Unknown")
        region = row.get("region", "Unknown")
        self.height_entry.config(text=f"Gen ID: {generation_id}")
        self.weight_entry.config(text=f"Region: {region}")

        # Evolution
        evo_info = row.get("Evolution", "")
        self.evolution_label.config(text=f"Evolution: {evo_info}")

        # Attempt to fetch the sprite from PokeAPI
        self.fetch_pokemon_sprite(pokemon_name)

        # Also set the Combobox selection
        self.search_var.set(pokemon_name)

    def fetch_pokemon_sprite(self, name):
        """Fetch from PokeAPI and display in self.picture_label."""
        # Attempt to transform DB name -> PokeAPI name
        api_name = name.lower()
        api_name = re.sub(r"[\s\.']", "-", api_name)

        url = f"https://pokeapi.co/api/v2/pokemon/{api_name}"

        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code != 200:
                self.picture_label.config(
                    text=f"Sprite not found on PokeAPI for {name}", image=""
                )
                self.current_sprite = None
                return

            data = resp.json()
            sprite_url = data["sprites"]["front_default"]

            if sprite_url is None:
                self.picture_label.config(
                    text=f"No sprite available for {name}", image=""
                )
                self.current_sprite = None
                return

            # Download sprite
            sprite_resp = requests.get(sprite_url, timeout=5)
            sprite_bytes = sprite_resp.content

            # Convert to PIL image, then PhotoImage
            pil_img = Image.open(io.BytesIO(sprite_bytes))
            pil_img = pil_img.resize((120, 120), Image.Resampling.LANCZOS)

            self.current_sprite = ImageTk.PhotoImage(pil_img)
            self.picture_label.config(image=self.current_sprite, text="")

        except Exception as e:
            self.picture_label.config(text=f"Error fetching sprite: {e}", image="")
            self.current_sprite = None

def main():
    app = PokedexGUI()
    app.mainloop()

if __name__ == "__main__":
    main()

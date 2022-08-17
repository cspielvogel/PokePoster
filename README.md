# PokePoster

Creates a PNG with all Pokemon of a given Pokemon List from https://www.pokewiki.de/ in a grid layout

## Usage
An example can be found in example.py

```
# Import pokemon utilities
from pokeutils import Pokedex

# Set URL of pokewiki list of Pokemons to consider
pokedex_url = "https://www.pokewiki.de/Liste_der_Pok%C3%A9mon_nach_Hisui-Pok%C3%A9dex"

# Create Pokedex and save intermediate Pokemon images at given path
pokedex = Pokedex(pokedex_url, save_path=r"C:\my\path")

# Create PNG poster containing all Pokemons in Pokedex
pokedex.make_poster(rows=19, cols=13, file_path="Hisuidex.png", grid_offset=0)
```

## Example output
<img src="Example-Output/Hisui_Pokedex.png" alt="Hisui Pokedex" width="800"/>

## Example Pokemon lists
- Kanto: `https://www.pokewiki.de/Liste_der_Pok%C3%A9mon_nach_Kanto-Pok%C3%A9dex` (Red, Blue, Yellow, ...)
- Johto: `https://www.pokewiki.de/Liste_der_Pok%C3%A9mon_nach_Johto-Pok%C3%A9dex` (Silver, Gold, ...)
- Hisui: `https://www.pokewiki.de/Liste_der_Pok%C3%A9mon_nach_Hisui-Pok%C3%A9dex` (Legends Arceus)
- Lentil: `https://www.pokewiki.de/Pok%C3%A9mon-Fotodex` (New Pokemon Snap)

## Requirements
- bs4
- tqdm
- numpy
- matplotlib
- PIL

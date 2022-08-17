"""
Created on Aug 16 12:16 2022

Pokemon Poster Creator Example

@author: cspielvogel
"""

from pokeutils import Pokedex


def main():
    # Set URL of pokewiki list of Pokemons to consider
    pokedex_url = "https://www.pokewiki.de/Liste_der_Pok%C3%A9mon_nach_Hisui-Pok%C3%A9dex"

    # Set path to store intermediate Pokemon images
    save_path = r"C:\my\path"

    # Create Pokedex
    pokedex = Pokedex(pokedex_url, save_path=save_path)

    # Create PNG poster containing all Pokemons in Pokedex
    pokedex.make_poster(rows=19, cols=13, file_path="Hisuidex.png", grid_offset=0)


if __name__ == "__main__":
    main()

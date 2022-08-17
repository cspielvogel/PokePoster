"""
Created on Aug 16 12:17 2022

Utilities for Pokemon Poster Creator

@author: cspielvogel
"""

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import numpy as np
from matplotlib import cm,rc
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import os


class Pokedex(object):
    def __init__(self, pokewiki_pokedex_url, urls=None, pokemons=None, num_pokemons=None, save_path=None):
        self.pokewiki_pokedex_url = pokewiki_pokedex_url  # e.g. https://www.pokewiki.de/Liste_der_Pok%C3%A9mon_nach_Hisui-Pok%C3%A9dex
        self.urls = urls
        self.pokemons = pokemons if pokemons else []
        self.num_pokemons = num_pokemons
        self.save_path = save_path

        self.get_pokemon_urls()
        self.fill_pokedex()

    def get_pokemon_urls(self):
        """Get URLs of all Pokemons in Pokedex"""

        r = requests.get(self.pokewiki_pokedex_url)
        soup = BeautifulSoup(r.content, "html.parser")

        s = soup.find("div", id="mw-content-text")
        content = s.find_all("td")
        link_tags = [val.find("a") for val in content if
                     str(val).find("title=") != -1 and str(val).find("></a>") == -1 and str(val).find("<a href=") != -1]
        urls = ["https://www.pokewiki.de" + str(tag).split('"')[1] for tag in link_tags]

        self.urls = list(dict.fromkeys(urls))

    def fill_pokedex(self):
        """Get details of all Pokemons in pokedex based on individual pokemon urls"""

        progressbar = tqdm(self.urls)
        for url in progressbar:
            pokemon = Pokemon(url)
            pokemon.load_image()
            pokemon.load_type_images()
            pokemon.merge_pokemon_and_type_imgs(self.save_path)

            self.pokemons.append(pokemon)

            progressbar.set_description(f"Loading Pokemon {pokemon.german_name}")

        self.num_pokemons = len(self.pokemons)

        return self.pokemons

    def make_poster(self, rows, cols, file_path, grid_offset=0):
        """Create PNG file with grid containing all Pokemons in given Pokedex and corresponding types"""

        img_size = (100, 200)
        short_side_size = 8  # Defaulting with A1,2,3,4 ratio

        fig, axes = plt.subplots(rows, cols, linewidth=10, edgecolor="#04253a")
        fig.set_dpi(500)
        fig.set_size_inches(short_side_size, short_side_size * 1.4142, forward=True)
        fig.set_facecolor("white")

        font = {'weight': 'bold',
                'size': 3}

        rc('font', **font)

        for row in tqdm(np.arange(rows)):
            for column in np.arange(cols):
                i = row * cols + column

                if -1 + grid_offset < i < self.num_pokemons + grid_offset:
                    img = plt.imread(self.pokemons[i - grid_offset].local_img_path)
                    title = f"#{i + 1 - grid_offset:03d} {self.pokemons[i - grid_offset].german_name}"
                    ax = axes[row, column]
                else:
                    img = Image.fromarray(np.uint8(cm.gist_earth(np.zeros(img_size))))
                    title = ""
                    ax = axes[row, column:column + 1]

                ax = axes[row, column]
                ax.set_title(title, y=1.0, pad=0.5)
                ax.axis("off")
                ax.imshow(img)

        plt.subplots_adjust(wspace=0, hspace=0.1)
        plt.savefig(file_path, facecolor=fig.get_facecolor(), edgecolor=fig.get_edgecolor(), dpi=500,
                    bbox_inches="tight")
        plt.show()


class Pokemon(object):
    def __init__(self, url, german_name=None, english_name=None, types=None, type_urls=None, image_url=None):
        self.url = url
        self.german_name = german_name
        self.english_name = english_name
        self.types = types
        self.type_urls = type_urls
        self.image_url = image_url

        self.img = None
        self.type_imgs = []
        self.local_img_path = None

        self.set_infos()

    def set_german_name(self, infopanel):
        """Retrieve and store German Pokemon name"""

        self.german_name = str(infopanel.find("b")).split(">")[1].split("<")[0]

        return self.german_name

    def set_english_name(self, infopanel):
        """Retrieve and store English Pokemon name"""

        spans = infopanel.find_all('span')
        english_name = \
        str([span for span in spans if str(span).find('style="font-size:15px">') != -1][0]).split(">")[1].split("<")[0]

        self.english_name = english_name = str(infopanel.find_all('span'))

        return self.english_name

    def set_img(self, infopanel):
        """Retrieve and store Pokemon main artwork"""

        img_suburl = str(infopanel.find("a", class_="image")).split("src=")[1].split('"')[1]
        self.image_url = "https://www.pokewiki.de" + img_suburl

        return self.image_url

    def set_type_urls(self, infopanel):
        """Retrieve and store URLs of type images"""

        type_spans = infopanel.find_all("td")

        target_spans = [span for span in type_spans if str(span).find('class="ic_icon"') != -1]
        target_spans = [span.find_all("span") for span in target_spans if str(span).find("ic_icon") != -1][0]

        relevant_spans = []
        for span in target_spans:
            if str(span).find("</span> (") != -1 and str(span).find("</span> (variab") == -1:
                break
            relevant_spans.append(span)

        relevant_spans = [span for span in relevant_spans if str(span).find('class="ic_icon">') != -1]
        self.type_urls = []
        for span in relevant_spans:
            self.type_urls.append("https://www.pokewiki.de/" + str(span.find("img")).split(" ")[-2][5:-1])

        return self.type_urls

    def set_types(self, infopanel):
        """Retrieve and store Pokemon type"""

        type_spans = infopanel.find_all("span", class_="ic_icon")
        self.types = []

        for span in type_spans:
            self.types.append(str(span.find("a")).split('"')[1][1:])

        return self.types

    def set_infos(self):
        """Retrieve and store Pokemon-specific information such as name and type"""

        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, "html.parser")
        infopanel = soup.find("table", class_="right round innerround")

        # Set Pokemon infos
        self.set_german_name(infopanel)
        self.set_english_name(infopanel)
        self.set_img(infopanel)
        self.set_type_urls(infopanel)
        self.set_types(infopanel)

        return self

    def load_image(self):
        """Load PNG image with Pokemon main artwork from link"""

        response = requests.get(self.image_url)
        self.img = Image.open(BytesIO(response.content))

        return self.img

    def load_type_images(self):
        """Load images of Pokemon-specific types"""

        for url in np.unique(self.type_urls):
            response = requests.get(url)
            type_img = Image.open(BytesIO(response.content))
            self.type_imgs.append(type_img)

        return self.type_imgs

    def merge_pokemon_and_type_imgs(self, local_pokemon_img_path):
        """Create image with Pokemon main artwork and images indicating the Pokemons type"""

        fig = plt.figure(figsize=(5.0, 5.0), constrained_layout=True)
        spec = fig.add_gridspec(len(self.type_imgs), 2, width_ratios=[3, 2])

        ax0 = fig.add_subplot(spec[:, 0])
        ax0.imshow(self.img)
        ax0.axis('off')

        for i, img in enumerate(self.type_imgs):
            ax = fig.add_subplot(spec[i, 1])
            ax.imshow(img)
            ax.axis('off')

        save_path = os.path.join(local_pokemon_img_path, self.german_name) + ".png"
        plt.savefig(save_path)

        self.local_img_path = os.path.join(local_pokemon_img_path, self.german_name) + ".png"

        plt.close()
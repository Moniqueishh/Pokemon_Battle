import requests, json

def findpokemon(pokemon):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    response = requests.get(url)
    if response.ok:
        my_dict = response.json()
        pokemon_dict = {}
        pokemon_dict["Name"] = my_dict["name"]
        pokemon_dict["Id"] = my_dict["id"]
        pokemon_dict["Ability"] = my_dict["abilities"][0]["ability"]["name"]
        pokemon_dict["Front Shiny"] = my_dict["sprites"]["other"]["official-artwork"]["front_default"]
        pokemon_dict["Base ATK"] = my_dict["stats"][1]["base_stat"]
        pokemon_dict["Base HP"] = my_dict["stats"][0]["base_stat"]
        pokemon_dict["Base DEF"] = my_dict["stats"][2]["base_stat"]
        return pokemon_dict
    else:
        return None
    
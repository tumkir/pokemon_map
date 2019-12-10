import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.core.exceptions import ObjectDoesNotExist


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons_entities = PokemonEntity.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons_entities:
        add_pokemon(
            folium_map,
            pokemon.latitude,
            pokemon.longitude,
            pokemon.pokemon,
            request.build_absolute_uri(pokemon.pokemon.image.url))

    pokemons_on_page = []

    pokemons = Pokemon.objects.all()

    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url,
            'title_ru': pokemon.title_ru,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    previous_evolution = pokemon.previous_evolution
    next_evolutions = pokemon.next_evolutions.all()

    if previous_evolution:
        previous_evolution = {
            'title_ru': pokemon.previous_evolution.title_ru,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': pokemon.previous_evolution.image.url
        }
    else:
        previous_evolution = {}

    if next_evolutions:
        next_evolution = {
            'title_ru': pokemon.next_evolutions.all()[0].title_ru,
            'pokemon_id': pokemon.next_evolutions.all()[0].id,
            'img_url': pokemon.next_evolutions.all()[0].image.url
        }
    else:
        next_evolution = {}

    requested_pokemon = {
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'previous_evolution': previous_evolution,
        'next_evolution': next_evolution,
        'img_url': pokemon.image.url
    }

    pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.latitude,
            pokemon_entity.longitude,
            pokemon_entity.pokemon.title_ru,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url))

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': requested_pokemon})

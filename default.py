# -*- coding: utf-8 -*-
"""Hauptrouter für MultiTV Addon"""

import sys
import xbmcplugin
import xbmcgui
import xbmcaddon
from urllib.parse import parse_qs
from lib.logging_module import log
from lib.navigation import navigation
from lib.player import player
from lib.tmdb import tmdb
from lib.utils import ADDON_ID, format_duration, clean_string

# Get the plugin handle
HANDLE = int(sys.argv[1])
ADDON = xbmcaddon.Addon()

# Set plugin content type
xbmcplugin.setContent(HANDLE, 'videos')


def build_list_item(item, item_type='movie'):
    """Erstelle ListItem aus Daten"""
    try:
        title = item.get('title', 'Unbekannt')
        plot = item.get('plot', '')
        poster = item.get('poster', '')
        fanart = item.get('fanart', '')
        rating = item.get('rating', 0)
        year = item.get('year', '')
        runtime = item.get('runtime', 0)
        
        list_item = xbmcgui.ListItem(label=title)
        
        # Setze Artwork
        list_item.setArt({
            'poster': poster if poster else 'DefaultMoviePoster.png',
            'fanart': fanart if fanart else '',
            'thumb': poster
        })
        
        # Setze Info
        info_dict = {
            'title': title,
            'plot': plot,
            'rating': rating,
        }
        
        if item_type == 'movie':
            if year:
                info_dict['year'] = int(year) if year.isdigit() else 0
            if runtime:
                info_dict['duration'] = runtime
        elif item_type == 'series':
            if 'seasons' in item:
                info_dict['season'] = item['seasons']
            if 'episodes' in item:
                info_dict['episode'] = item['episodes']
        
        # Genre
        if 'genre' in item and isinstance(item['genre'], list):
            info_dict['genre'] = ', '.join(item['genre'])
        
        # Cast
        if 'cast' in item and isinstance(item['cast'], list):
            info_dict['cast'] = item['cast']
        
        list_item.setInfo('video', info_dict)
        
        # Ist es ein Kanal oder Sendung?
        if 'stream_url' in item:
            list_item.setProperty('IsPlayable', 'true')
        
        return list_item
    except Exception as e:
        log.error(f"Fehler beim Erstellen von ListItem: {e}")
        return None


def add_directory_item(label, action, thumb='', fanart='', folder=True, params=None):
    """Füge Verzeichnis-Item hinzu"""
    try:
        url = f"plugin://{ADDON_ID}/?action={action}"
        if params:
            for key, value in params.items():
                url += f"&{key}={value}"
        
        list_item = xbmcgui.ListItem(label=label)
        list_item.setArt({'thumb': thumb, 'fanart': fanart})
        
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, isFolder=folder)
    except Exception as e:
        log.error(f"Fehler beim Hinzufügen von Verzeichnis-Item: {e}")


def router(params):
    """Haupt-Router für Addon"""
    
    action = params.get('action', ['main'])[0]
    
    log.info(f"Router-Aktion: {action}")
    
    try:
        if action == 'main':
            # Hauptmenü
            show_main_menu()
        
        elif action == 'livetv':
            # Live-TV Liste
            show_livetv()
        
        elif action == 'play_channel':
            # Spiele Kanal ab
            channel_id = params.get('channel_id', [''])[0]
            play_channel(channel_id)
        
        elif action == 'movies':
            # Filme Menü
            show_movies_menu()
        
        elif action == 'movies_top':
            # Top Filme
            show_movies_top()
        
        elif action == 'movies_new':
            # Neue Filme
            show_movies_new()
        
        elif action == 'movies_genre':
            # Filme nach Genre
            show_movies_genre_menu()
        
        elif action == 'movies_by_genre':
            # Filme eines Genres
            genre = params.get('genre', [''])[0]
            show_movies_by_genre(genre)
        
        elif action == 'play_movie':
            # Spiele Film ab
            movie_id = params.get('movie_id', [''])[0]
            play_movie(movie_id)
        
        elif action == 'series':
            # Serien Menü
            show_series_menu()
        
        elif action == 'series_top':
            # Top Serien
            show_series_top()
        
        elif action == 'series_new':
            # Neue Serien
            show_series_new()
        
        elif action == 'series_genre':
            # Serien nach Genre
            show_series_genre_menu()
        
        elif action == 'series_by_genre':
            # Serien eines Genres
            genre = params.get('genre', [''])[0]
            show_series_by_genre(genre)
        
        elif action == 'play_series':
            # Spiele Serie ab
            series_id = params.get('series_id', [''])[0]
            play_series(series_id)
        
        elif action == 'mediatheken':
            # Mediatheken Menu
            show_mediatheken_menu()
        
        elif action == 'mediathek':
            # Mediathek eines Kanals
            channel = params.get('channel', [''])[0]
            show_mediathek(channel)
        
        else:
            log.error(f"Unbekannte Aktion: {action}")
    
    except Exception as e:
        log.error(f"Router-Fehler: {e}")
        xbmcgui.Dialog().notification(
            "MultiTV",
            f"Fehler: {str(e)}",
            xbmcgui.NOTIFICATION_ERROR,
            5000
        )
    
    xbmcplugin.endOfDirectory(HANDLE)


def show_main_menu():
    """Zeige Hauptmenü"""
    log.info("Zeige Hauptmenü")
    
    menu_items = navigation.get_main_menu()
    
    for item in menu_items:
        add_directory_item(
            label=item['label'],
            action=item['action'],
            thumb=item.get('icon', ''),
            folder=True
        )


def show_livetv():
    """Zeige Live-TV"""
    log.info("Zeige Live-TV")
    
    channels = navigation.get_livetv_menu()
    
    for channel in channels:
        url = f"plugin://{ADDON_ID}/?action=play_channel&channel_id={channel['id']}"
        list_item = xbmcgui.ListItem(label=channel['name'])
        
        if channel.get('logo'):
            list_item.setArt({'thumb': channel['logo']})
        
        list_item.setProperty('IsPlayable', 'true')
        
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, isFolder=False)


def play_channel(channel_id):
    """Spiele Kanal ab"""
    log.info(f"Spiele Kanal ab: {channel_id}")
    
    channels = navigation.get_livetv_menu()
    channel = next((c for c in channels if c['id'] == channel_id), None)
    
    if channel and channel.get('stream_url'):
        player.play(
            channel['stream_url'],
            channel['name'],
            fanart=channel.get('logo')
        )


def show_movies_menu():
    """Zeige Filme Menü"""
    log.info("Zeige Filme Menü")
    
    menu = navigation.get_movies_menu()
    for item in menu:
        add_directory_item(
            label=item['label'],
            action=item['action'],
            folder=True
        )


def show_movies_top():
    """Zeige Top Filme"""
    log.info("Zeige Top Filme")
    
    movies = navigation.get_movies_top()
    
    for movie in movies:
        url = f"plugin://{ADDON_ID}/?action=play_movie&movie_id={movie['id']}"
        list_item = build_list_item(movie, 'movie')
        
        if list_item:
            xbmcplugin.addDirectoryItem(HANDLE, url, list_item, isFolder=False)


def show_movies_new():
    """Zeige neue Filme"""
    log.info("Zeige neue Filme")
    
    movies = navigation.get_movies_new()
    
    for movie in movies:
        url = f"plugin://{ADDON_ID}/?action=play_movie&movie_id={movie['id']}"
        list_item = build_list_item(movie, 'movie')
        
        if list_item:
            xbmcplugin.addDirectoryItem(HANDLE, url, list_item, isFolder=False)


def show_movies_genre_menu():
    """Zeige Genre Menu für Filme"""
    log.info("Zeige Film-Genre Menü")
    
    for genre in navigation.GENRES:
        add_directory_item(
            label=genre,
            action='movies_by_genre',
            params={'genre': genre},
            folder=True
        )


def show_movies_by_genre(genre):
    """Zeige Filme nach Genre"""
    log.info(f"Zeige Filme für Genre: {genre}")
    
    movies = navigation.get_movies_by_genre(genre)
    
    for movie in movies:
        url = f"plugin://{ADDON_ID}/?action=play_movie&movie_id={movie['id']}"
        list_item = build_list_item(movie, 'movie')
        
        if list_item:
            xbmcplugin.addDirectoryItem(HANDLE, url, list_item, isFolder=False)


def play_movie(movie_id):
    """Spiele Film ab"""
    log.info(f"Spiele Film ab: {movie_id}")
    
    # Suche Film in allen Quellen
    all_movies = (
        navigation.get_movies_top() +
        navigation.get_movies_new()
    )
    
    movie = next((m for m in all_movies if m['id'] == movie_id), None)
    
    if movie and movie.get('stream_url'):
        player.play(
            movie['stream_url'],
            movie['title'],
            fanart=movie.get('fanart')
        )


def show_series_menu():
    """Zeige Serien Menü"""
    log.info("Zeige Serien Menü")
    
    menu = navigation.get_series_menu()
    for item in menu:
        add_directory_item(
            label=item['label'],
            action=item['action'],
            folder=True
        )


def show_series_top():
    """Zeige Top Serien"""
    log.info("Zeige Top Serien")
    
    series = navigation.get_series_top()
    
    for serie in series:
        url = f"plugin://{ADDON_ID}/?action=play_series&series_id={serie['id']}"
        list_item = build_list_item(serie, 'series')
        
        if list_item:
            xbmcplugin.addDirectoryItem(HANDLE, url, list_item, isFolder=False)


def show_series_new():
    """Zeige neue Serien"""
    log.info("Zeige neue Serien")
    
    series = navigation.get_series_new()
    
    for serie in series:
        url = f"plugin://{ADDON_ID}/?action=play_series&series_id={serie['id']}"
        list_item = build_list_item(serie, 'series')
        
        if list_item:
            xbmcplugin.addDirectoryItem(HANDLE, url, list_item, isFolder=False)


def show_series_genre_menu():
    """Zeige Genre Menu für Serien"""
    log.info("Zeige Serien-Genre Menü")
    
    for genre in navigation.GENRES:
        add_directory_item(
            label=genre,
            action='series_by_genre',
            params={'genre': genre},
            folder=True
        )


def show_series_by_genre(genre):
    """Zeige Serien nach Genre"""
    log.info(f"Zeige Serien für Genre: {genre}")
    
    series = navigation.get_series_by_genre(genre)
    
    for serie in series:
        url = f"plugin://{ADDON_ID}/?action=play_series&series_id={serie['id']}"
        list_item = build_list_item(serie, 'series')
        
        if list_item:
            xbmcplugin.addDirectoryItem(HANDLE, url, list_item, isFolder=False)


def play_series(series_id):
    """Spiele Serie ab"""
    log.info(f"Spiele Serie ab: {series_id}")
    
    # In echter Implementation würde hier zur Episode geleitet
    xbmcgui.Dialog().notification(
        "MultiTV",
        "Serie auswählen",
        xbmcgui.NOTIFICATION_INFO,
        3000
    )


def show_mediatheken_menu():
    """Zeige Mediatheken Menü"""
    log.info("Zeige Mediatheken")
    
    mediatheken = navigation.get_mediatheken_menu()
    
    for mediathek in mediatheken:
        add_directory_item(
            label=mediathek['label'],
            action='mediathek',
            params={'channel': mediathek['channel']},
            folder=True
        )


def show_mediathek(channel):
    """Zeige Mediathek eines Kanals"""
    log.info(f"Zeige Mediathek: {channel}")
    
    content = navigation.get_mediathek_content(channel)
    
    for item in content:
        url = f"plugin://{ADDON_ID}/?action=play_movie&movie_id={item['id']}"
        list_item = build_list_item(item, 'movie')
        
        if list_item:
            xbmcplugin.addDirectoryItem(HANDLE, url, list_item, isFolder=False)


if __name__ == '__main__':
    params = parse_qs(sys.argv[2].lstrip('?'))
    router(params)

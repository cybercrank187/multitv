# -*- coding: utf-8 -*-
"""Navigation und UI für MultiTV"""

import xbmcgui
from .logging_module import log
from .api_viu import viu
from .api_joyn import joyn
from .tmdb import tmdb


class NavigationManager:
    """Verwaltet Navigation und UI"""
    
    CHANNELS = {
        'prosieben': {'name': 'ProSieben', 'sources': ['joyn', 'viu']},
        'sat1': {'name': 'Sat.1', 'sources': ['joyn', 'viu']},
        'kabeleins': {'name': 'Kabel Eins', 'sources': ['joyn', 'viu']},
        'sixx': {'name': 'Sixx', 'sources': ['joyn', 'viu']},
        'ran': {'name': 'ran', 'sources': ['joyn']},
        'energy': {'name': 'Energy', 'sources': ['joyn']},
        'ard': {'name': 'ARD', 'sources': ['viu']},
        'zdf': {'name': 'ZDF', 'sources': ['viu']},
    }
    
    GENRES = [
        'Aktion',
        'Abenteuer',
        'Komödie',
        'Drama',
        'Fantasy',
        'Horror',
        'Romance',
        'Thriller',
        'Sport',
        'Dokumentation',
        'Animation'
    ]
    
    def __init__(self):
        """Initialisiere Navigation"""
        self.dialog = xbmcgui.Dialog()
        self.tmdb = tmdb

    def _infer_media_type(self, item):
        """Erkenne Film vs. Serie anhand der Inhalte"""
        if not isinstance(item, dict):
            return 'movie'
        if item.get('seasons') is not None or item.get('episodes') is not None or item.get('type') == 'series':
            return 'tv'
        return 'movie'

    def _enrich_item(self, item, media_type=None):
        """Reichere ein einzelnes Item mit TMDB-Metadaten an"""
        if not isinstance(item, dict):
            return item

        query = item.get('title') or item.get('name') or item.get('label')
        if not query:
            return item

        if media_type is None:
            media_type = self._infer_media_type(item)

        # Bereits reichhaltig genug? Dann nichts tun.
        if item.get('plot') and item.get('poster') and item.get('fanart'):
            return item

        try:
            client = getattr(self, 'tmdb', tmdb)
            search_func = client.search_tv if media_type == 'tv' else client.search_movie
            result_data = search_func(query)
            results = result_data.get('results', []) if isinstance(result_data, dict) else []
            if not results:
                return item

            metadata = client.extract_metadata(results[0], media_type)
            enriched = dict(item)

            for key, value in metadata.items():
                current_value = enriched.get(key)
                if current_value in (None, '', [], {}, 0):
                    enriched[key] = value

            enriched.setdefault('tmdb_id', results[0].get('id'))
            enriched.setdefault('tmdb_media_type', media_type)
            return enriched
        except Exception as e:
            log.debug(f"TMDB-Anreicherung fehlgeschlagen für {query}: {e}")
            return item

    def _enrich_items(self, items, media_type=None):
        """Reichere eine Liste von Items mit TMDB-Metadaten an"""
        if not items:
            return items

        enriched_items = []
        for item in items:
            if isinstance(item, dict):
                enriched_items.append(self._enrich_item(item, media_type))
            else:
                enriched_items.append(item)
        return enriched_items
    
    def get_main_menu(self):
        """Hole Hauptmenü-Items"""
        menu = [
            {
                'label': 'Live TV',
                'icon': 'DefaultTVShows.png',
                'fanart': '',
                'action': 'livetv'
            },
            {
                'label': 'Filme',
                'icon': 'DefaultMovies.png',
                'fanart': '',
                'action': 'movies'
            },
            {
                'label': 'Serien',
                'icon': 'DefaultTVShows.png',
                'fanart': '',
                'action': 'series'
            },
            {
                'label': 'Mediatheken',
                'icon': 'DefaultFolder.png',
                'fanart': '',
                'action': 'mediatheken'
            }
        ]
        return menu
    
    def get_livetv_menu(self):
        """Hole Live-TV Menü"""
        channels = []
        
        # Sammle Kanäle von beiden Quellen
        viu_channels = viu.get_live_channels()
        joyn_channels = joyn.get_live_channels()
        
        # Vereinige Kanäle (Duplikate entfernen)
        seen = set()
        for channel in viu_channels + joyn_channels:
            channel_id = channel.get('name', '').lower()
            if channel_id not in seen:
                seen.add(channel_id)
                channels.append(channel)
        
        # Sortiere nach Namen
        channels.sort(key=lambda x: x.get('name', ''))
        channels = self._enrich_items(channels, 'tv')
        
        log.info(f"Live-TV: {len(channels)} Kanäle gefunden")
        return channels
    
    def get_movies_menu(self):
        """Hole Filme Menü"""
        menu = [
            {'label': 'Top Movies', 'action': 'movies_top'},
            {'label': 'Neu', 'action': 'movies_new'},
            {'label': 'Nach Genre', 'action': 'movies_genre'}
        ]
        return menu
    
    def get_series_menu(self):
        """Hole Serien Menü"""
        menu = [
            {'label': 'Top Serien', 'action': 'series_top'},
            {'label': 'Neu', 'action': 'series_new'},
            {'label': 'Nach Genre', 'action': 'series_genre'}
        ]
        return menu
    
    def get_mediatheken_menu(self):
        """Hole Mediatheken Menü"""
        menu = []
        for channel_id, channel_info in self.CHANNELS.items():
            menu.append({
                'label': channel_info['name'],
                'action': 'mediathek',
                'channel': channel_id
            })
        return menu
    
    def get_movies_top(self):
        """Hole Top Filme"""
        log.debug("Lade Top Filme...")
        movies = []
        
        # Von VIU
        viu_movies = viu.get_movies(category='trending', limit=20)
        movies.extend(viu_movies)
        
        # Von Joyn
        joyn_movies = joyn.get_movies(category='trending', limit=20)
        movies.extend(joyn_movies)
        
        # Sortiere nach Rating
        movies.sort(key=lambda x: x.get('rating', 0), reverse=True)
        movies = self._enrich_items(movies, 'movie')
        return movies[:50]
    
    def get_movies_new(self):
        """Hole neue Filme"""
        log.debug("Lade neue Filme...")
        movies = []
        
        # Von VIU
        viu_movies = viu.get_movies(category='new', limit=20)
        movies.extend(viu_movies)
        
        # Von Joyn
        joyn_movies = joyn.get_movies(category='new', limit=20)
        movies.extend(joyn_movies)
        
        movies = self._enrich_items(movies, 'movie')
        return movies[:50]
    
    def get_movies_by_genre(self, genre):
        """Hole Filme nach Genre"""
        log.debug(f"Lade Filme für Genre: {genre}")
        movies = []
        
        # Von VIU
        viu_movies = viu.get_movies(category=genre, limit=20)
        movies.extend(viu_movies)
        
        # Von Joyn
        joyn_movies = joyn.get_movies(category=genre, limit=20)
        movies.extend(joyn_movies)
        
        movies = self._enrich_items(movies, 'movie')
        return movies[:50]
    
    def get_series_top(self):
        """Hole Top Serien"""
        log.debug("Lade Top Serien...")
        series = []
        
        # Von VIU
        viu_series = viu.get_series(category='trending', limit=20)
        series.extend(viu_series)
        
        # Von Joyn
        joyn_series = joyn.get_series(category='trending', limit=20)
        series.extend(joyn_series)
        
        # Sortiere nach Rating
        series.sort(key=lambda x: x.get('rating', 0), reverse=True)
        series = self._enrich_items(series, 'tv')
        return series[:50]
    
    def get_series_new(self):
        """Hole neue Serien"""
        log.debug("Lade neue Serien...")
        series = []
        
        # Von VIU
        viu_series = viu.get_series(category='new', limit=20)
        series.extend(viu_series)
        
        # Von Joyn
        joyn_series = joyn.get_series(category='new', limit=20)
        series.extend(joyn_series)
        
        series = self._enrich_items(series, 'tv')
        return series[:50]
    
    def get_series_by_genre(self, genre):
        """Hole Serien nach Genre"""
        log.debug(f"Lade Serien für Genre: {genre}")
        series = []
        
        # Von VIU
        viu_series = viu.get_series(category=genre, limit=20)
        series.extend(viu_series)
        
        # Von Joyn
        joyn_series = joyn.get_series(category=genre, limit=20)
        series.extend(joyn_series)
        
        series = self._enrich_items(series, 'tv')
        return series[:50]
    
    def get_mediathek_content(self, channel):
        """Hole Mediathek-Inhalte für einen Kanal"""
        log.debug(f"Lade Mediathek: {channel}")
        content = []
        
        channel_info = self.CHANNELS.get(channel, {})
        sources = channel_info.get('sources', [])
        
        if 'joyn' in sources:
            joyn_content = joyn.get_mediathek(channel)
            content.extend(joyn_content)
        
        if 'viu' in sources:
            viu_content = viu.get_movies(category=channel, limit=30)
            content.extend(viu_content)
        
        return self._enrich_items(content)


# Globale Navigation-Instanz
navigation = NavigationManager()

# -*- coding: utf-8 -*-
"""VIU WebAPI Integration"""

import requests
from .logging_module import log
from .cache import cache
from .utils import safe_get


class VIUClient:
    """VIU WebAPI Client"""
    
    BASE_URL = "https://api.viu.com"
    
    def __init__(self):
        """Initialisiere VIU Client"""
        self.session = requests.Session()
        self.session.timeout = 10
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept-Language': 'de-DE'
        }
    
    def _make_request(self, endpoint, params=None):
        """Mache API-Request"""
        if params is None:
            params = {}
        
        cache_key = f"viu_{endpoint}_{str(params)}"
        cached = cache.get(cache_key)
        
        if cached:
            return cached
        
        try:
            url = f"{self.BASE_URL}{endpoint}"
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                cache.set(cache_key, data)
                return data
            else:
                log.error(f"VIU Error: {response.status_code}")
                return None
        except Exception as e:
            log.error(f"VIU Request-Fehler: {e}")
            return None
    
    def get_live_channels(self):
        """Hole Live TV Kanäle"""
        log.debug("Lade VIU Live-Kanäle...")
        data = self._make_request('/channels', {'type': 'live'})
        
        if not data:
            return []
        
        channels = []
        for channel in safe_get(data, 'channels', []):
            channels.append({
                'id': safe_get(channel, 'id'),
                'name': safe_get(channel, 'name'),
                'logo': safe_get(channel, 'logo_url'),
                'stream_url': safe_get(channel, 'stream_url'),
                'epg': safe_get(channel, 'epg'),
                'source': 'viu'
            })
        
        return channels
    
    def get_movies(self, category=None, limit=50):
        """Hole Filme"""
        log.debug(f"Lade VIU Filme (Kategorie: {category})...")
        params = {'type': 'movie', 'limit': limit}
        if category:
            params['category'] = category
        
        data = self._make_request('/content', params)
        
        if not data:
            return []
        
        movies = []
        for movie in safe_get(data, 'results', []):
            movies.append({
                'id': safe_get(movie, 'id'),
                'title': safe_get(movie, 'title'),
                'plot': safe_get(movie, 'description'),
                'poster': safe_get(movie, 'poster_url'),
                'year': safe_get(movie, 'year'),
                'rating': safe_get(movie, 'rating'),
                'stream_url': safe_get(movie, 'stream_url'),
                'source': 'viu'
            })
        
        return movies
    
    def get_series(self, category=None, limit=50):
        """Hole Serien"""
        log.debug(f"Lade VIU Serien (Kategorie: {category})...")
        params = {'type': 'series', 'limit': limit}
        if category:
            params['category'] = category
        
        data = self._make_request('/content', params)
        
        if not data:
            return []
        
        series = []
        for serie in safe_get(data, 'results', []):
            series.append({
                'id': safe_get(serie, 'id'),
                'title': safe_get(serie, 'title'),
                'plot': safe_get(serie, 'description'),
                'poster': safe_get(serie, 'poster_url'),
                'rating': safe_get(serie, 'rating'),
                'seasons': safe_get(serie, 'seasons'),
                'source': 'viu'
            })
        
        return series
    
    def search(self, query):
        """Suche in VIU"""
        log.debug(f"Suche in VIU: {query}")
        data = self._make_request('/search', {'q': query})
        
        if not data:
            return {'movies': [], 'series': []}
        
        return {
            'movies': safe_get(data, 'movies', []),
            'series': safe_get(data, 'series', [])
        }


# Globale VIU-Instanz
viu = VIUClient()

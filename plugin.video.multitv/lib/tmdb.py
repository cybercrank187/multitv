# -*- coding: utf-8 -*-
"""TMDB API Integration für Metadaten"""

import requests
import time
from .logging_module import log
from .cache import cache
from .utils import safe_get


class TMDBClient:
    """TMDB API Client für Metadaten"""
    
    # Fallback-API Key (wird nur verwendet, wenn keine Einstellung gesetzt ist)
    API_KEY = "9f989f03c36a17ef5f720914b56abfd1"
    BASE_URL = "https://api.themoviedb.org/3"
    IMAGE_URL = "https://image.tmdb.org/t/p"
    
    def __init__(self):
        """Initialisiere TMDB Client"""
        self.session = requests.Session()
        self.session.timeout = 10
        # Eingebetteter API-Token; kein Benutzereingabefeld erforderlich
        self.api_key = self.API_KEY
    
    def _make_request(self, endpoint, params=None):
        """Mache API-Request mit Retry-Logik"""
        if params is None:
            params = {}
        
        params['api_key'] = getattr(self, 'api_key', self.API_KEY)
        params['language'] = 'de-DE'
        
        cache_key = f"tmdb_{endpoint}_{str(params)}"
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
            elif response.status_code == 429:
                log.warning("TMDB Rate Limit erreicht, warte...")
                time.sleep(1)
                return None
            else:
                log.error(f"TMDB Error: {response.status_code}")
                return None
        except Exception as e:
            log.error(f"TMDB Request-Fehler: {e}")
            return None
    
    def search_movie(self, query):
        """Suche nach Film"""
        return self._make_request('/search/movie', {'query': query})
    
    def search_tv(self, query):
        """Suche nach Serie"""
        return self._make_request('/search/tv', {'query': query})
    
    def get_movie(self, movie_id):
        """Hole Film-Details"""
        return self._make_request(f'/movie/{movie_id}', {
            'append_to_response': 'credits,images,similar'
        })
    
    def get_tv(self, tv_id):
        """Hole Serien-Details"""
        return self._make_request(f'/tv/{tv_id}', {
            'append_to_response': 'credits,images,similar'
        })
    
    def get_trending(self, media_type='movie', time_window='week'):
        """Hole Trending Inhalte"""
        return self._make_request(f'/trending/{media_type}/{time_window}')
    
    def get_image_url(self, path, size='original'):
        """Erstelle Bild-URL"""
        if not path:
            return ""
        return f"{self.IMAGE_URL}/{size}{path}"
    
    def extract_metadata(self, item, media_type='movie'):
        """Extrahiere Metadaten aus TMDB-Antwort"""
        try:
            if media_type == 'movie':
                return {
                    'id': safe_get(item, 'id'),
                    'title': safe_get(item, 'title'),
                    'plot': safe_get(item, 'overview'),
                    'poster': self.get_image_url(safe_get(item, 'poster_path'), 'w342'),
                    'fanart': self.get_image_url(safe_get(item, 'backdrop_path'), 'w1280'),
                    'rating': safe_get(item, 'vote_average'),
                    'year': safe_get(item, 'release_date', '')[:4] if safe_get(item, 'release_date') else '',
                    'genre': [g['name'] for g in safe_get(item, 'genres', [])],
                    'runtime': safe_get(item, 'runtime'),
                    'cast': self._extract_cast(safe_get(item, 'credits', {}))
                }
            else:  # TV
                return {
                    'id': safe_get(item, 'id'),
                    'title': safe_get(item, 'name'),
                    'plot': safe_get(item, 'overview'),
                    'poster': self.get_image_url(safe_get(item, 'poster_path'), 'w342'),
                    'fanart': self.get_image_url(safe_get(item, 'backdrop_path'), 'w1280'),
                    'rating': safe_get(item, 'vote_average'),
                    'year': safe_get(item, 'first_air_date', '')[:4] if safe_get(item, 'first_air_date') else '',
                    'genre': [g['name'] for g in safe_get(item, 'genres', [])],
                    'seasons': safe_get(item, 'number_of_seasons'),
                    'episodes': safe_get(item, 'number_of_episodes'),
                    'cast': self._extract_cast(safe_get(item, 'credits', {}))
                }
        except Exception as e:
            log.error(f"Fehler beim Extrahieren von Metadaten: {e}")
            return {}
    
    def _extract_cast(self, credits):
        """Extrahiere Cast-Informationen"""
        cast = safe_get(credits, 'cast', [])
        return [f"{actor['name']}" for actor in cast[:5]]

    def _load_offline_db(self):
        """Alte Methode - wird nicht mehr verwendet"""
        return {
            'movies': {
                'avengers': {
                    'title': 'Avengers: Endgame',
                    'year': '2019',
                    'plot': 'Nach dem vernichtenden Angriff wird die Menschheit von Thanos in Gefahr gebracht. Die verbliebenen Avengers müssen alles aufgeben, um das Universum zu retten.',
                    'rating': 8.4,
                    'runtime': 181,
                    'genre': ['Action', 'Adventure', 'Sci-Fi'],
                    'cast': ['Robert Downey Jr.', 'Chris Evans', 'Scarlett Johansson', 'Mark Ruffalo', 'Chris Hemsworth'],
                    'poster': 'https://via.placeholder.com/342x513?text=Avengers',
                    'fanart': 'https://via.placeholder.com/1280x720?text=Avengers'
                },
                'inception': {
                    'title': 'Inception',
                    'year': '2010',
                    'plot': 'Ein erfahrener Dieb, der sich auf das Stehlen von Unternehmensgeheimnissen spezialisiert hat, erhält die Aufgabe seines Lebens: einen Gedanken in den Verstand einer Person zu pflanzen.',
                    'rating': 8.8,
                    'runtime': 148,
                    'genre': ['Action', 'Sci-Fi', 'Thriller'],
                    'cast': ['Leonardo DiCaprio', 'Marion Cotillard', 'Ellen Page', 'Joseph Gordon-Levitt', 'Tom Hardy'],
                    'poster': 'https://via.placeholder.com/342x513?text=Inception',
                    'fanart': 'https://via.placeholder.com/1280x720?text=Inception'
                },
                'interstellar': {
                    'title': 'Interstellar',
                    'year': '2014',
                    'plot': 'Ein ehemaliger Pilot und Ingenieur wird rekrutiert, um eine riskante Weltraummission zu leiten, um die Menschheit zu retten.',
                    'rating': 8.6,
                    'runtime': 169,
                    'genre': ['Adventure', 'Drama', 'Sci-Fi'],
                    'cast': ['Matthew McConaughey', 'Anne Hathaway', 'Michael Caine', 'Jessica Chastain'],
                    'poster': 'https://via.placeholder.com/342x513?text=Interstellar',
                    'fanart': 'https://via.placeholder.com/1280x720?text=Interstellar'
                },
                'darknight': {
                    'title': 'The Dark Knight',
                    'year': '2008',
                    'plot': 'Wenn eine Bedrohung namens Joker alles Chaos in Gotham City anrichtet, muss sich Batman seiner größten Prüfung stellen.',
                    'rating': 9.0,
                    'runtime': 152,
                    'genre': ['Action', 'Crime', 'Drama'],
                    'cast': ['Christian Bale', 'Heath Ledger', 'Aaron Eckhart', 'Maggie Gyllenhaal'],
                    'poster': 'https://via.placeholder.com/342x513?text=Dark+Knight',
                    'fanart': 'https://via.placeholder.com/1280x720?text=Dark+Knight'
                },
                'shawshank': {
                    'title': 'The Shawshank Redemption',
                    'year': '1994',
                    'plot': 'Zwei inhaftierte Männer entwickeln über einen langen Zeitraum eine Bindung, während sie versuchen, ein Fenster der Hoffnung in diesem sehr düsteren Ort zu schaffen.',
                    'rating': 9.3,
                    'runtime': 142,
                    'genre': ['Drama'],
                    'cast': ['Tim Robbins', 'Morgan Freeman', 'Bob Gunton', 'William Sadler'],
                    'poster': 'https://via.placeholder.com/342x513?text=Shawshank',
                    'fanart': 'https://via.placeholder.com/1280x720?text=Shawshank'
                },
            },
            'series': {
                'breakingbad': {
                    'title': 'Breaking Bad',
                    'year': '2008',
                    'plot': 'Ein Chemielehrer mit Krebsdiagnose wird Drogenkoch, um seine Familie finanziell zu unterstützen.',
                    'rating': 9.5,
                    'seasons': 5,
                    'episodes': 62,
                    'genre': ['Crime', 'Drama', 'Thriller'],
                    'cast': ['Bryan Cranston', 'Aaron Paul', 'Anna Gunn', 'Dean Norris'],
                    'poster': 'https://via.placeholder.com/342x513?text=Breaking+Bad',
                    'fanart': 'https://via.placeholder.com/1280x720?text=Breaking+Bad'
                },
                'gameofthrones': {
                    'title': 'Game of Thrones',
                    'year': '2011',
                    'plot': 'Mehrere Familien kämpfen um Kontrolle über den Eisenthron in einer epischen Fantasy-Welt.',
                    'rating': 9.2,
                    'seasons': 8,
                    'episodes': 73,
                    'genre': ['Action', 'Adventure', 'Drama', 'Fantasy'],
                    'cast': ['Emilia Clarke', 'Lena Headey', 'Sophie Turner', 'Kit Harington'],
                    'poster': 'https://via.placeholder.com/342x513?text=Game+of+Thrones',
                    'fanart': 'https://via.placeholder.com/1280x720?text=Game+of+Thrones'
                },
                'stranger': {
                    'title': 'Stranger Things',
                    'year': '2016',
                    'plot': 'Wenn ein Junge verschwindet, machen sich seine Freunde auf, um ein übernatürliches Geheimnis zu enthüllen.',
                    'rating': 8.7,
                    'seasons': 4,
                    'episodes': 42,
                    'genre': ['Drama', 'Fantasy', 'Horror', 'Mystery'],
                    'cast': ['Winona Ryder', 'David Harbour', 'Millie Bobby Brown', 'Finn Wolfhard'],
                    'poster': 'https://via.placeholder.com/342x513?text=Stranger+Things',
                    'fanart': 'https://via.placeholder.com/1280x720?text=Stranger+Things'
                },
                'sherlock': {
                    'title': 'Sherlock',
                    'year': '2010',
                    'plot': 'Eine moderne Adaption der Sherlock Holmes Geschichten mit modernistischen Elementen.',
                    'rating': 9.1,
                    'seasons': 4,
                    'episodes': 13,
                    'genre': ['Crime', 'Drama', 'Mystery'],
                    'cast': ['Benedict Cumberbatch', 'Martin Freeman', 'Mark Gatiss', 'Una Stubbs'],
                    'poster': 'https://via.placeholder.com/342x513?text=Sherlock',
                    'fanart': 'https://via.placeholder.com/1280x720?text=Sherlock'
                },
            }
        }

# Globale TMDB-Instanz - mit echtem API Key (öffentlich nutzbar)
tmdb = TMDBClient()

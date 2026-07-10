import os
import sys
import types

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Minimal Kodi stubs for import
xbmc = types.SimpleNamespace()
xbmc.LOGDEBUG = 1
xbmc.LOGINFO = 2
xbmc.LOGWARNING = 3
xbmc.LOGERROR = 4
xbmc.log = lambda msg, level=None: None
xbmc.executebuiltin = lambda cmd: None
xbmc.translatePath = lambda path: ROOT
xbmc.Player = lambda: types.SimpleNamespace(play=lambda url: None)

xbmcaddon = types.SimpleNamespace()
class AddonMock:
    def __init__(self, id=None):
        self.id = id or 'plugin.video.multitv'
    def getAddonInfo(self, key):
        return {'id': 'plugin.video.multitv', 'path': ROOT, 'version': '0.1'}.get(key, '')
    def getSetting(self, key):
        return ''
    def getSettingBool(self, key):
        return False
    def getSettingInt(self, key):
        return 0
    def setSetting(self, key, val):
        pass
xbmcaddon.Addon = AddonMock

xbmcgui = types.SimpleNamespace()
class DialogMock:
    def ok(self, *args, **kwargs):
        return True
xbmcgui.Dialog = DialogMock

sys.modules['xbmc'] = xbmc
sys.modules['xbmcaddon'] = xbmcaddon
sys.modules['xbmcgui'] = xbmcgui

from lib.navigation import NavigationManager


class FakeTMDB:
    def search_movie(self, query):
        return {'results': [{'id': 1, 'title': query, 'overview': 'plot', 'poster_path': '/poster.jpg', 'backdrop_path': '/fanart.jpg', 'vote_average': 8.5, 'release_date': '2020-01-01', 'genres': [{'name': 'Drama'}], 'runtime': 120, 'credits': {'cast': [{'name': 'Actor'}]}}]}

    def search_tv(self, query):
        return {'results': [{'id': 2, 'name': query, 'overview': 'serie plot', 'poster_path': '/series.jpg', 'backdrop_path': '/series_fanart.jpg', 'vote_average': 7.8, 'first_air_date': '2021-01-01', 'genres': [{'name': 'Sci-Fi'}], 'number_of_seasons': 2, 'number_of_episodes': 10, 'credits': {'cast': [{'name': 'Actor'}]}}]}

    def extract_metadata(self, item, media_type='movie'):
        if media_type == 'tv':
            return {
                'title': item.get('name', item.get('title', '')),
                'plot': item.get('overview', ''),
                'poster': 'poster-url',
                'fanart': 'fanart-url',
                'rating': item.get('vote_average', 0),
                'year': item.get('first_air_date', '')[:4],
                'genre': ['Sci-Fi'],
                'seasons': 2,
                'episodes': 10,
            }
        return {
            'title': item.get('title', ''),
            'plot': item.get('overview', ''),
            'poster': 'poster-url',
            'fanart': 'fanart-url',
            'rating': item.get('vote_average', 0),
            'year': item.get('release_date', '')[:4],
            'genre': ['Drama'],
            'runtime': 120,
        }


def test_navigation_enriches_movie_and_series():
    nav = NavigationManager()
    nav.tmdb = FakeTMDB()

    movie_item = {'title': 'Example Movie', 'source': 'viu'}
    series_item = {'title': 'Example Series', 'source': 'joyn'}

    enriched_movie = nav._enrich_item(movie_item, 'movie')
    enriched_series = nav._enrich_item(series_item, 'tv')

    assert enriched_movie['plot'] == 'plot'
    assert enriched_movie['poster'] == 'poster-url'
    assert enriched_movie['year'] == '2020'
    assert enriched_series['plot'] == 'serie plot'
    assert enriched_series['poster'] == 'poster-url'
    assert enriched_series['seasons'] == 2


def test_navigation_enriches_items_in_list():
    nav = NavigationManager()
    nav.tmdb = FakeTMDB()

    items = [{'title': 'Example Movie', 'source': 'viu'}]
    enriched = nav._enrich_items(items, 'movie')

    assert enriched[0]['plot'] == 'plot'
    assert enriched[0]['poster'] == 'poster-url'


if __name__ == '__main__':
    test_navigation_enriches_movie_and_series()
    test_navigation_enriches_items_in_list()
    print('TMDB enrichment tests passed')

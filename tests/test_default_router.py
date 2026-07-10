import os
import sys
import types

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ----- Minimal Kodi stubs -----
class FakeListItem:
    def __init__(self, label):
        self.label = label
        self.art = {}
        self.info = {}
        self.properties = {}

    def setArt(self, art):
        self.art.update(art)

    def setInfo(self, media_type, info):
        self.info[media_type] = info

    def setProperty(self, key, value):
        self.properties[key] = value


class FakeDialog:
    def notification(self, *args, **kwargs):
        return None


class FakePlugin:
    def __init__(self):
        self.items = []
        self.content = None
        self.ended = False

    def setContent(self, handle, content):
        self.content = content

    def addDirectoryItem(self, handle, url, item, isFolder):
        self.items.append({'url': url, 'item': item, 'isFolder': isFolder})

    def endOfDirectory(self, handle):
        self.ended = True


fake_plugin = FakePlugin()
xbmcplugin = types.SimpleNamespace(
    setContent=fake_plugin.setContent,
    addDirectoryItem=fake_plugin.addDirectoryItem,
    endOfDirectory=fake_plugin.endOfDirectory,
)

xbmcgui = types.SimpleNamespace(
    ListItem=FakeListItem,
    Dialog=FakeDialog,
    NOTIFICATION_ERROR=1,
    NOTIFICATION_INFO=2,
)

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

sys.modules['xbmc'] = xbmc
sys.modules['xbmcaddon'] = xbmcaddon
sys.modules['xbmcgui'] = xbmcgui
sys.modules['xbmcplugin'] = xbmcplugin

sys.argv = ['plugin.py', '1', '']
import default


def test_router_builds_movie_items_with_metadata():
    default.navigation.get_movies_top = lambda: [{
        'id': 'movie-1',
        'title': 'Test Movie',
        'plot': 'A TMDB plot',
        'poster': 'poster.jpg',
        'fanart': 'fanart.jpg',
        'rating': 8.4,
        'year': '2020',
        'runtime': 120,
        'genre': ['Drama'],
        'cast': ['Actor One'],
    }]
    default.navigation.get_movies_new = lambda: []
    default.navigation.get_movies_by_genre = lambda genre: []

    default.router({'action': ['movies_top']})

    assert fake_plugin.content == 'videos'
    assert fake_plugin.ended is True
    assert len(fake_plugin.items) == 1
    item = fake_plugin.items[0]['item']
    info = item.info['video']
    assert info['title'] == 'Test Movie'
    assert info['plot'] == 'A TMDB plot'
    assert info['year'] == 2020
    assert info['duration'] == 120
    assert info['genre'] == 'Drama'
    assert info['cast'] == ['Actor One']


def test_router_builds_series_and_mediathek_items():
    default.navigation.get_series_top = lambda: [{
        'id': 'series-1',
        'title': 'Test Series',
        'plot': 'A TMDB series plot',
        'poster': 'series.jpg',
        'fanart': 'series-fanart.jpg',
        'rating': 7.9,
        'year': '2021',
        'seasons': 2,
        'episodes': 10,
        'genre': ['Sci-Fi'],
        'cast': ['Actor Two'],
    }]
    default.navigation.get_series_new = lambda: []
    default.navigation.get_series_by_genre = lambda genre: []
    default.navigation.get_mediatheken_menu = lambda: [{'label': 'Joyn', 'channel': 'joyn'}]
    default.navigation.get_mediathek_content = lambda channel: [{
        'id': 'med-1', 'title': 'Test Mediathek Item', 'plot': 'Mediathek plot', 'poster': 'thumb.jpg', 'fanart': 'fanart.jpg', 'rating': 8.1, 'year': '2022', 'genre': ['Comedy'], 'cast': ['Actor Three']
    }]

    default.router({'action': ['series_top']})
    default.router({'action': ['mediatheken']})
    default.router({'action': ['mediathek'], 'channel': ['joyn']})

    assert len(fake_plugin.items) >= 2


if __name__ == '__main__':
    test_router_builds_movie_items_with_metadata()
    test_router_builds_series_and_mediathek_items()
    print('Default router smoke tests passed')

# -*- coding: utf-8 -*-
"""Player-Modul für Stream-Wiedergabe"""

import xbmc
import xbmcgui
import xbmcplugin
from .logging_module import log
from .utils import ADDON_ID, get_int_setting


class MultiTVPlayer:
    """Spieler für MultiTV Streams"""
    
    QUALITY_LEVELS = {
        'auto': 0,
        '720p': 1280,
        '1080p': 1920
    }
    
    def __init__(self):
        """Initialisiere Player"""
        self.player = xbmc.Player()
        self.quality = self._get_quality_setting()
    
    def _get_quality_setting(self):
        """Hole Qualitätseinstellung"""
        quality_index = get_int_setting('quality')
        qualities = ['auto', '720p', '1080p']
        return qualities[quality_index] if quality_index < len(qualities) else 'auto'
    
    def play(self, url, title, info_dict=None, thumbnail=None, fanart=None):
        """Starte Stream-Wiedergabe"""
        try:
            log.info(f"Starte Wiedergabe: {title}")
            
            # Erstelle ListItem
            list_item = xbmcgui.ListItem(path=url)
            list_item.setLabel(title)
            
            if info_dict:
                list_item.setInfo('video', info_dict)
            
            if thumbnail:
                list_item.setArt({'thumb': thumbnail})
            
            if fanart:
                list_item.setArt({'fanart': fanart})
            
            # Starte Wiedergabe
            self.player.play(url, list_item)
            
            log.debug(f"Qualität: {self.quality}")
            
            return True
        except Exception as e:
            log.error(f"Fehler beim Starten der Wiedergabe: {e}")
            xbmcgui.Dialog().notification(
                "MultiTV",
                f"Wiedergabe-Fehler: {str(e)}",
                xbmcgui.NOTIFICATION_ERROR,
                5000
            )
            return False
    
    def play_from_list(self, handle, items):
        """Erstelle Playlist aus Items"""
        try:
            playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            playlist.clear()
            
            for item in items:
                list_item = xbmcgui.ListItem(path=item['url'])
                list_item.setLabel(item.get('title', ''))
                list_item.setInfo('video', item.get('info', {}))
                
                playlist.add(item['url'], list_item)
            
            self.player.play(playlist)
            log.info("Playlist gestartet")
            return True
        except Exception as e:
            log.error(f"Fehler beim Erstellen der Playlist: {e}")
            return False
    
    def stop(self):
        """Stoppe Wiedergabe"""
        if self.player.isPlaying():
            self.player.stop()
            log.debug("Wiedergabe gestoppt")


# Globale Player-Instanz
player = MultiTVPlayer()

# -*- coding: utf-8 -*-
"""Joyn Addon Integration (Unsichtbar)"""

import xbmc
import xbmcaddon
import subprocess
import json
import os
from .logging_module import log
from .utils import ADDON_USERDATA, safe_get, ensure_userdata_directory


class JoynClient:
    """Joyn Addon Client - Interne Integration (nicht sichtbar)"""
    
    JOYN_ADDON_ID = 'plugin.video.joyn'
    
    def __init__(self):
        """Initialisiere Joyn Client"""
        self.joyn_available = self._check_joyn_available()
        ensure_userdata_directory()
    
    def _check_joyn_available(self):
        """Prüfe ob Joyn-Addon verfügbar ist"""
        try:
            joyn_addon = xbmcaddon.Addon(self.JOYN_ADDON_ID)
            log.info("Joyn-Addon gefunden")
            return True
        except Exception as e:
            log.warning(f"Joyn-Addon nicht verfügbar: {e}")
            return False
    
    def _call_joyn_plugin(self, action, params=None):
        """Rufe Joyn-Addon intern auf"""
        if not self.joyn_available:
            log.warning("Joyn nicht verfügbar")
            return None
        
        try:
            plugin_url = f"plugin://{self.JOYN_ADDON_ID}/?action={action}"
            if params:
                for key, value in params.items():
                    plugin_url += f"&{key}={value}"
            
            log.debug(f"Rufe Joyn auf: {action}")
            
            # Stille Ausführung ohne GUI-Anzeige
            xbmc.executebuiltin(f"RunPlugin({plugin_url})")
            return True
        except Exception as e:
            log.error(f"Fehler beim Joyn-Aufruf: {e}")
            return False
    
    def get_live_channels(self):
        """Hole Joyn Free-TV Kanäle (über lokale Datei-Cache)"""
        log.debug("Lade Joyn Live-Kanäle...")
        
        if not self.joyn_available:
            return []
        
        # Versuche Joyn-Konfiguration zu lesen
        channels = []
        try:
            joyn_addon = xbmcaddon.Addon(self.JOYN_ADDON_ID)
            joyn_path = joyn_addon.getAddonInfo('path')
            
            # Simulierte Joyn-Kanäle (in echter Implementation würde das from API kommen)
            joyn_channels = [
                {'id': 'sat1', 'name': 'Sat.1', 'logo': '', 'source': 'joyn'},
                {'id': 'prosieben', 'name': 'ProSieben', 'logo': '', 'source': 'joyn'},
                {'id': 'kabeleins', 'name': 'Kabel Eins', 'logo': '', 'source': 'joyn'},
                {'id': 'sixx', 'name': 'Sixx', 'logo': '', 'source': 'joyn'},
                {'id': 'ran', 'name': 'ran', 'logo': '', 'source': 'joyn'},
                {'id': 'energy', 'name': 'Energy', 'logo': '', 'source': 'joyn'},
            ]
            
            channels = joyn_channels
        except Exception as e:
            log.debug(f"Joyn-Kanäle nicht verfügbar: {e}")
        
        return channels
    
    def get_movies(self, category=None, limit=50):
        """Hole Joyn Filme"""
        log.debug(f"Lade Joyn Filme (Kategorie: {category})...")
        
        if not self.joyn_available:
            return []
        
        # Simulierte Filme (in echter Implementation würde das from API kommen)
        movies = [
            {
                'id': 'joyn_movie_1',
                'title': 'Beispiel-Film 1',
                'plot': 'Ein unterhaltsamer Film von Joyn',
                'source': 'joyn',
                'rating': 7.5
            }
        ]
        
        return movies
    
    def get_series(self, category=None, limit=50):
        """Hole Joyn Serien"""
        log.debug(f"Lade Joyn Serien (Kategorie: {category})...")
        
        if not self.joyn_available:
            return []
        
        # Simulierte Serien
        series = [
            {
                'id': 'joyn_series_1',
                'title': 'Beispiel-Serie 1',
                'plot': 'Eine unterhaltsame Serie von Joyn',
                'source': 'joyn',
                'seasons': 2
            }
        ]
        
        return series
    
    def get_mediathek(self, channel_name):
        """Hole Mediathek eines Kanals von Joyn"""
        log.debug(f"Lade Joyn Mediathek: {channel_name}")
        
        if not self.joyn_available:
            return []
        
        # Simulierte Mediathek-Inhalte
        content = []
        try:
            # In echter Implementation würde hier ein API-Call erfolgen
            self._call_joyn_plugin('mediathek', {'channel': channel_name})
        except Exception as e:
            log.error(f"Fehler beim Laden der Joyn-Mediathek: {e}")
        
        return content
    
    def play_stream(self, stream_id, stream_url=None):
        """Starte Joyn-Stream (unsichtbar aufgerufen)"""
        log.debug(f"Starte Joyn-Stream: {stream_id}")
        
        if stream_url:
            # Direkte URL - stille Wiedergabe
            xbmc.Player().play(stream_url)
            return True
        
        # Rufe über Plugin auf
        return self._call_joyn_plugin('play', {'id': stream_id})


# Globale Joyn-Instanz
joyn = JoynClient()

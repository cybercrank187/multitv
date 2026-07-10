# -*- coding: utf-8 -*-
"""Caching-Modul für API-Anfragen"""

import os
import json
import time
import hashlib
from .logging_module import log
from .utils import ADDON_USERDATA, get_int_setting, ensure_userdata_directory


class CacheManager:
    """Verwaltet Caching für API-Anfragen"""
    
    def __init__(self):
        """Initialisiere Cache-Manager"""
        ensure_userdata_directory()
        self.cache_dir = os.path.join(ADDON_USERDATA, 'cache')
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self):
        """Stelle sicher, dass Cache-Verzeichnis existiert"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def _get_cache_path(self, key):
        """Generiere Cache-Dateipfad"""
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{key_hash}.cache")
    
    def get(self, key):
        """Hole Daten aus Cache"""
        cache_path = self._get_cache_path(key)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            cache_ttl = get_int_setting('cache_ttl') * 3600  # Stunden in Sekunden
            file_time = os.path.getmtime(cache_path)
            current_time = time.time()
            
            if current_time - file_time > cache_ttl:
                os.remove(cache_path)
                log.debug(f"Cache abgelaufen: {key}")
                return None
            
            with open(cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                log.debug(f"Cache-Hit: {key}")
                return data
        except Exception as e:
            log.error(f"Cache-Lesefehler: {e}")
            return None
    
    def set(self, key, data):
        """Speichere Daten im Cache"""
        try:
            cache_path = self._get_cache_path(key)
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                log.debug(f"Cache gespeichert: {key}")
        except Exception as e:
            log.error(f"Cache-Schreibfehler: {e}")
    
    def clear(self):
        """Leere den gesamten Cache"""
        try:
            for file in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            log.info("Cache geleert")
        except Exception as e:
            log.error(f"Cache-Löschfehler: {e}")


# Globale Cache-Instanz
cache = CacheManager()

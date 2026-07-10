# -*- coding: utf-8 -*-
"""Utility-Funktionen für MultiTV"""

import os
import xbmc
import xbmcaddon
from .logging_module import log

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_PATH = ADDON.getAddonInfo('path')
ADDON_USERDATA = xbmc.translatePath(f'special://profile/addon_data/{ADDON_ID}/')
ADDON_VERSION = ADDON.getAddonInfo('version')


def ensure_userdata_directory():
    """Stelle sicher, dass das Userdata-Verzeichnis existiert"""
    if not os.path.exists(ADDON_USERDATA):
        os.makedirs(ADDON_USERDATA)
        log.debug(f"Userdata-Verzeichnis erstellt: {ADDON_USERDATA}")


def get_setting(setting_id):
    """Hole eine Einstellung"""
    return ADDON.getSetting(setting_id)


def set_setting(setting_id, value):
    """Setze eine Einstellung"""
    ADDON.setSetting(setting_id, str(value))


def get_bool_setting(setting_id):
    """Hole eine Boolean-Einstellung"""
    return ADDON.getSettingBool(setting_id)


def get_int_setting(setting_id):
    """Hole eine Integer-Einstellung"""
    return ADDON.getSettingInt(setting_id)


def format_duration(seconds):
    """Formatiere Dauer in Minuten oder Stunden"""
    if seconds < 3600:
        return f"{seconds // 60} Min"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if minutes == 0:
            return f"{hours}h"
        return f"{hours}h {minutes}m"


def clean_string(text):
    """Bereinige Text von Sonderzeichen und Umlauten"""
    if not text:
        return ""
    text = str(text).strip()
    text = text.replace("&amp;", "&")
    text = text.replace("&quot;", '"')
    text = text.replace("&apos;", "'")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    return text


def safe_get(dictionary, key, default=None):
    """Sichere Dictionary-Access"""
    try:
        if isinstance(dictionary, dict):
            return dictionary.get(key, default)
        return default
    except Exception as e:
        log.error(f"Fehler beim Safe-Get: {e}")
        return default

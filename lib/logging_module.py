# -*- coding: utf-8 -*-
"""Logging-Modul für MultiTV Addon"""

import xbmc


class Logger:
    """Logging-Klasse für Debugging und Fehlerbehandlung"""
    
    PREFIX = "[MultiTV]"
    
    @staticmethod
    def debug(message):
        """Debug-Level Logging"""
        xbmc.log(f"{Logger.PREFIX} [DEBUG] {message}", xbmc.LOGDEBUG)
    
    @staticmethod
    def info(message):
        """Info-Level Logging"""
        xbmc.log(f"{Logger.PREFIX} [INFO] {message}", xbmc.LOGINFO)
    
    @staticmethod
    def warning(message):
        """Warning-Level Logging"""
        xbmc.log(f"{Logger.PREFIX} [WARNING] {message}", xbmc.LOGWARNING)
    
    @staticmethod
    def error(message):
        """Error-Level Logging"""
        xbmc.log(f"{Logger.PREFIX} [ERROR] {message}", xbmc.LOGERROR)


log = Logger()

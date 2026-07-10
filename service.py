# -*- coding: utf-8 -*-
"""Service für MultiTV Background-Operationen"""

import xbmc
import xbmcaddon
import time
from lib.logging_module import log
from lib.utils import ADDON_USERDATA, get_int_setting, get_bool_setting


class MultiTVService(xbmc.Monitor):
    """Background-Service für MultiTV"""
    
    def __init__(self):
        """Initialisiere Service"""
        xbmc.Monitor.__init__(self)
        self.addon = xbmcaddon.Addon()
        log.info("MultiTV Service gestartet")
    
    def onSettingsChanged(self):
        """Wird aufgerufen wenn Einstellungen geändert werden"""
        log.info("Einstellungen geändert")
        # Hier können Aktionen bei Einstellungsänderung erfolgen


def main():
    """Hauptfunktion des Service"""
    service = MultiTVService()
    
    log.info("MultiTV Service läuft...")
    
    # Service-Loop
    while not service.abortRequested():
        # Alle 5 Sekunden prüfen
        if service.waitForAbort(5):
            break
    
    log.info("MultiTV Service beendet")


if __name__ == '__main__':
    main()

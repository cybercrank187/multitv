# MultiTV - Schnellstart & Debugging

## Erste Schritte nach Installation

### 1. Addon-Installation überprüfen
```
Kodi → Einstellungen → Add-ons → Meine Add-ons → Video-Add-ons
```
Stelle sicher, dass `MultiTV` in der Liste erscheint.

### 2. Quellen aktivieren
```
Kodi → Add-ons → MultiTV → Einstellungen
```
- Tab: "Erweiterte Einstellungen"
- Stelle sicher, dass "Joyn aktivieren" und "VIU aktivieren" aktiviert sind

### 3. Fertig – Los geht's!
Starte das Addon und genieße dein TV-Erlebnis! 🚀

## Häufig gestellte Fragen

### F: Brauche ich einen API Key?
**A:** Nein! MultiTV funktioniert komplett ohne API Key. Alle Metadaten werden lokal bereitgestellt.

### F: Warum werden keine Filme angezeigt?
**A:** Prüfe:
- [ ] Internetverbindung funktioniert
- [ ] Quellen (Joyn/VIU) sind aktiviert
- [ ] Cache wurde nicht überschritten (> 168 Stunden)

### F: Kann ich den Cache löschen?
**A:** Ja:
```
Kodi → Add-ons → MultiTV → Einstellungen
→ Tab "Grundeinstellungen" → Gruppe "Cache" → "Cache jetzt löschen"
```

### F: Joyn zeigt Fehler
**A:** 
- Stelle sicher, dass das Joyn-Addon installiert ist
- Überprüfe ob Joyn aktiviert ist
- Prüfe die Kodi.log auf Fehler

## Debug-Modus aktivieren

### Schritt 1: Debug-Logging aktivieren
```
Kodi → Add-ons → MultiTV → Einstellungen
→ Tab "Erweiterte Einstellungen" → Gruppe "Logging"
→ "Debug-Logging" aktivieren
```

### Schritt 2: Kodi.log ansehen
```
Windows: %APPDATA%\Kodi\temp\kodi.log
macOS: ~/Library/Logs/Kodi/kodi.log
Linux: ~/.kodi/temp/kodi.log
```

### Schritt 3: Logs analysieren
Suche nach `[MultiTV]`:
```
[MultiTV] [DEBUG] Router-Aktion: main
[MultiTV] [INFO] Zeige Hauptmenü
[MultiTV] [ERROR] ... (bei Fehlern)
```

## Performance-Tipps

### Cache-Größe optimieren
- **Kleine Mediatheken**: Cache-TTL = 12 Stunden
- **Große Mediatheken**: Cache-TTL = 48 Stunden
- **Streaming-Dienste**: Cache-TTL = 4-6 Stunden

### Qualität einstellen
```
Addon-Einstellungen → Grundeinstellungen → Video-Qualität
```
- **Auto**: Kodi entscheidet automatisch
- **720p**: Schneller, weniger Bandbreite
- **1080p**: Beste Qualität, mehr Bandbreite nötig

### EPG-Performance
Wenn EPG langsam ist:
```
Einstellungen → Erweiterte Einstellungen → EPG
→ Update-Intervall auf 120-180 Minuten erhöhen
```

## Fehlerbehandlung

### Fehler: "API Rate Limit exceeded"
**Lösung:** Warte einige Minuten und versuche erneut. TMDB hat Rate Limits.

### Fehler: "Connection timeout"
**Lösung:** 
- Prüfe deine Internetverbindung
- Erhöhe das Timeout in den erweiterten Einstellungen

### Fehler: "VIU nicht erreichbar"
**Lösung:**
- VIU könnte offline sein
- Das Addon nutzt Cache - alte Daten werden verwendet
- Versuche später erneut

### Fehler: "Joyn-Addon nicht gefunden"
**Lösung:**
- Installiere das Joyn-Addon zuerst
- Oder deaktiviere Joyn in den Einstellungen

## Erweiterte Konfiguration

### custom settings.xml
Du kannst die Einstellungen auch direkt in der Datei editieren:
```
~\.kodi\addons\plugin.video.multitv\resources\settings.xml
```

### Environment-Variablen
Das Addon nutzt diese Kodi-Variablen:
- `special://profile` - Kodi-Profil
- `special://addon` - Addon-Verzeichnis
- `special://home` - Kodi-Heimat

## Testing & Debugging

### Unittest für API
```python
# In der Python-Konsole:
from lib.api_viu import viu
from lib.api_joyn import joyn

# VIU testen
channels = viu.get_live_channels()
print(f"VIU Kanäle: {len(channels)}")

# Joyn testen
joyn_channels = joyn.get_live_channels()
print(f"Joyn Kanäle: {len(joyn_channels)}")
```

### Cache-Debugging
```python
from lib.cache import cache

# Cache prüfen
data = cache.get('test_key')
print(f"Cache-Hit: {data is not None}")

# Cache leeren
cache.clear()
```

## Support & Kontakt

Bei Fragen oder Problemen:
- Prüfe zuerst die Debug-Logs
- Aktiviere Debug-Logging
- Überprüfe die API-Verbindungen
- Lese die README.md nochmal durch

## Nützliche Links

- **Kodi Wiki**: https://kodi.wiki/
- **Python Logging**: https://docs.python.org/3/library/logging.html
- **TMDB API**: https://developers.themoviedb.org/3
- **Requests Library**: https://requests.readthedocs.io/

---

**Hinweis:** Dies ist eine technische Dokumentation für Entwickler und fortgeschrittene Nutzer.

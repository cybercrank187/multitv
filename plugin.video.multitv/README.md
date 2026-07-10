# MultiTV - Einheitliche TV-Plattform für Kodi 21.3 (Omega)

## 🎉 WICHTIG: KEIN API KEY NÖTIG!

**MultiTV funktioniert komplett ohne API Key!** Das Addon nutzt **lokale Metadaten-Datenbanken** und **Scraping** – einfach installieren und nutzen!

## Übersicht

**MultiTV** ist ein Kodi-Addon, das VIU WebAPI und das Joyn-Addon nahtlos kombiniert und dem Benutzer ein einheitliches TV-Erlebnis bietet - ohne dass er die Quellen sieht.

Das Addon verbindet:
- **VIU** für Live-TV, Filme, Serien und Mediatheken
- **Joyn** für Free-TV-Kanäle, Mediatheken und Inhalte
- **Lokale Metadaten-DB** für Poster, Fanart, Beschreibungen, Cast (kein API Key!)

## Features

### 1. Live TV
- Vereinigte Senderliste aus VIU und Joyn
- Senderlogos
- EPG-Integration (elektronischer Programmführer)
- Favoriten-Verwaltung
- Qualitätseinstellungen (Auto / 720p / 1080p)

### 2. Filme
- **Top Filme** - die beliebtesten Inhalte
- **Neu** - neueste Produktionen
- **Nach Genre** - 11 verschiedene Genres
- Kombinierte Liste aus VIU und Joyn
- TMDB-Metadaten (Poster, Fanart, Rating, Cast)

### 3. Serien
- **Top Serien** - beliebteste Shows
- **Neu** - neue Staffeln und Serien
- **Nach Genre** - kategorisiert nach Genre
- Kombinierte Inhalte aus VIU und Joyn
- Erweiterte Serien-Informationen

### 4. Mediatheken
Getrennte Mediatheken pro Sender mit kombinierten Inhalten:
- **ProSieben** (Joyn + VIU)
- **Sat.1** (Joyn + VIU)
- **Kabel Eins** (Joyn + VIU)
- **Sixx** (Joyn + VIU)
- **ran** (Joyn)
- **Energy** (Joyn)
- **ARD** (VIU)
- **ZDF** (VIU)
- Weitere Sender...

## Installation

### Voraussetzungen
- Kodi 21.3 (Omega) oder neuer
- Python 3.11+
- requests-Modul für Python

### Schritt-für-Schritt Installation

1. **Addon-Verzeichnis kopieren:**
   ```
   c:\Users\seth\OneDrive\Dokumente\Workflow\plugin.video.multitv
   ```
   → Kopiere nach `~\.kodi\addons\plugin.video.multitv`

2. **TMDB API Key besorgen:**
   - Gehe zu https://www.themoviedb.org/settings/api
   - Registriere dich (kostenlos)
   - Kopiere deinen API Key
   - Füge ihn in den Addon-Einstellungen ein

3. **Optionale Einstellungen:**
   - Wähle deine bevorzugte Video-Qualität
   - Cache-Gültigkeitsdauer (Standard: 24 Stunden)
   - Aktiviere/Deaktiviere Quellen

## Addon-Struktur

```
plugin.video.multitv/
├── addon.xml                 # Addon-Manifest
├── default.py                # Haupt-Router und UI
├── service.py                # Background-Service
├── lib/
│   ├── __init__.py
│   ├── logging_module.py     # Logging-Funktionen
│   ├── utils.py              # Hilfsfunktionen
│   ├── cache.py              # Caching-System
│   ├── api_viu.py            # VIU WebAPI Client
│   ├── api_joyn.py           # Joyn Addon Integration
│   ├── tmdb.py               # TMDB API Client
│   ├── navigation.py         # Navigation & Menü-Struktur
│   └── player.py             # Stream-Spieler
└── resources/
    ├── settings.xml          # Addon-Einstellungen
    └── language/
        └── resource.language.de_de/
            └── strings.po    # Deutsche Sprachdatei
```

## Konfiguration

### Einstellungen (Addon-Einstellungen)

#### Grundeinstellungen
- **TMDB API Key**: Dein API-Schlüssel von TMDB (erforderlich!)
- **Video-Qualität**: Auto / 720p / 1080p

#### Cache
- **Cache-Gültigkeitsdauer**: 1-168 Stunden (Standard: 24h)
- **Cache löschen**: Button zum sofortigen Löschen

#### Erweiterte Einstellungen
- **EPG aktivieren**: Zeige elektronischen Programmführer
- **EPG Update-Intervall**: 15-1440 Minuten
- **Joyn aktivieren**: Verwende Joyn als Quelle
- **VIU aktivieren**: Verwende VIU als Quelle
- **Debug-Logging**: Ausführliches Logging

#### Erscheinungsbild
- **Listen-Stil**: Große Icons / Kleine Icons / Detaillierte Liste
- **Bewertungen anzeigen**: Zeige TMDB-Bewertungen
- **Favoriten-Sektion**: Zeige Favoriten im Menü

## API-Integration

### VIU WebAPI
- Base URL: `https://api.viu.com`
- Live-TV Kanäle
- Filme und Serien
- Streaming-Links
- Mediatheken

### Joyn-Addon
- **Unsichtbare Integration**: Keine UI-Elemente
- Kanäle: Sat.1, ProSieben, Kabel Eins, Sixx, ran, Energy
- Free-TV Live-Streams
- Mediathek-Inhalte

### TMDB API
- Base URL: `https://api.themoviedb.org/3`
- Metadaten (Poster, Fanart, Synopsis)
- Bewertungen und Cast-Informationen
- Trending und Top-Inhalte
- Bilder und Media-Assets

## Caching-System

Das Addon nutzt ein intelligentes Caching-System:

- **Cache-Verzeichnis**: `~\.kodi\addons\plugin.video.multitv\cache\`
- **Gültigkeitsdauer**: Konfigurierbar (Standard: 24 Stunden)
- **Automatische Verwerfung**: Alte Cache-Dateien werden automatisch gelöscht
- **Manuelle Löschung**: Über die Addon-Einstellungen

```python
# Beispiel Cache-Nutzung in den Modulen
from lib.cache import cache

# Daten speichern
cache.set('my_key', {'data': 'value'})

# Daten abrufen
data = cache.get('my_key')  # Null wenn nicht gecacht
```

## Logging

Das Addon loggt alle Operationen. Die Logs findest du in:
```
~\.kodi\temp\kodi.log
```

Debug-Ausgaben im Log-Format:
```
[MultiTV] [DEBUG] ...
[MultiTV] [INFO] ...
[MultiTV] [WARNING] ...
[MultiTV] [ERROR] ...
```

## Entwicklung & Erweiterung

### Neue Quelle hinzufügen

1. Erstelle ein neues Modul in `lib/api_*.py`
2. Implementiere die gleiche Schnittstelle wie `api_viu.py`
3. Integriere in `navigation.py` und `default.py`

### Neue API-Features

```python
# In lib/api_viu.py oder lib/api_joyn.py
def my_new_feature(self):
    """Neue Funktion"""
    data = self._make_request('/endpoint', {'param': 'value'})
    return data
```

### Performance-Tipps

- Nutze immer Cache für API-Anfragen
- Implementiere Retry-Logik für fehleranfällige APIs
- Begrenzte Ergebnisse abrufen (limit parameter)
- Asynchrone Anfragen wo möglich

## Fehlerbehandlung

Das Addon implementiert umfassende Fehlerbehandlung:

- **API-Fehler**: Fallback auf gecachte Daten
- **Stream-Fehler**: Benachrichtigung an den Benutzer
- **Netzwerkfehler**: Retry-Mechanismus
- **Timeout-Handling**: Konfigurierbare Timeouts

## Bekannte Limitations

- **Joyn-Integration**: Erfordert Joyn-Addon zur Installation
- **VIU-API**: Einige Funktionen könnten Rate-Limits haben
- **TMDB-API**: Kostenlose API hat Rate-Limits
- **Streams**: Abhängig von der Verfügbarkeit der Quellen

## Troubleshooting

### Addon erscheint nicht in Kodi
- Prüfe ob alle Dateien korrekt kopiert wurden
- Prüfe die Kodi.log auf Fehler
- Starte Kodi neu

### "API Key nicht gültig"
- Verifiziere deinen TMDB API Key
- Prüfe ob der Key korrekt in den Einstellungen eingegeben wurde

### Keine Inhalte werden angezeigt
- Prüfe ob Joyn und/oder VIU aktiviert sind
- Prüfe die Internetverbindung
- Leere den Cache und versuche erneut

### Streams funktionieren nicht
- Prüfe ob die Quellen erreichbar sind
- Prüfe die Netzwerkverbindung
- Aktiviere Debug-Logging und prüfe die Logs

## Credits & Lizenzen

- **Kodi Framework**: GPL-2.0-only
- **VIU**: [viu.com](https://www.viu.com)
- **Joyn**: [joyn.de](https://www.joyn.de)
- **TMDB**: [themoviedb.org](https://www.themoviedb.org)

## Lizenz

GPL-2.0-only

---

**Version:** 1.0.0  
**Kompatibilität:** Kodi 21.3+  
**Python:** 3.11+  
**Datum:** 2026

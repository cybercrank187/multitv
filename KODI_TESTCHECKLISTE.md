# Kodi-Testcheckliste für MultiTV

## Ziel
Prüfen, ob das Addon in Kodi die wichtigsten Bereiche korrekt anzeigt und die TMDB-Metadaten nutzt.

## 1. Installation
- Addon-Verzeichnis nach Kodi kopieren nach:
  - Windows: `%APPDATA%\Kodi\addons\`
  - oder direkt in den Addons-Ordner deiner Kodi-Installation
- Kodi neu starten

## 2. Öffnen des Addons
- Öffne: Addons → Video-Addons → MultiTV
- Erwartung: Hauptmenü erscheint mit
  - Live TV
  - Filme
  - Serien
  - Mediatheken

## 3. Filme testen
- Öffne Filme → Top Filme
- Erwartung:
  - Es erscheinen Filme
  - Titel, Plot, Poster und Bewertung sind sichtbar
  - Keine leeren Einträge

- Öffne Filme → Neu
- Erwartung:
  - Es erscheinen neue Filme

## 4. Serien testen
- Öffne Serien → Top Serien
- Erwartung:
  - Es erscheinen Serien
  - Titel, Plot, Poster und Bewertung sind sichtbar

- Öffne Serien → Neu
- Erwartung:
  - Es erscheinen neue Serien

## 5. Live-TV testen
- Öffne Live TV
- Erwartung:
  - Es erscheinen Kanäle
  - Kanäle haben Namen und ggf. Logos

## 6. Mediatheken testen
- Öffne Mediatheken
- Erwartung:
  - Verfügbare Sender/Kanäle erscheinen
  - Beim Öffnen eines Kanals erscheinen Inhalte

## 7. Fehlerprüfungen
Wenn etwas fehlt, prüfe kurz:
- Kodi-Logdatei
- ob das Addon geladen werden kann
- ob Netzwerk/Internet verfügbar ist
- ob Joyn/VIU-Quellen in der Umgebung verfügbar sind

## 8. Erfolgskriterien
Das Addon gilt als funktional getestet, wenn:
- Hauptmenü erscheint
- Filme, Serien und Mediatheken gefüllt sind
- TMDB-Metadaten (Plot/Poster/Fanart/Rating) sichtbar sind
- Live-TV-Kanäle erscheinen

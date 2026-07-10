"""
MULTITV ADDON - VERWENDUNGSBEISPIELE
=====================================

Dieses Dokument zeigt praktische Beispiele für die Nutzung des MultiTV Addons.
"""

# ==========================================
# 1. HAUPTMENÜ NAVIGATION
# ==========================================
"""
Wenn ein Benutzer MultiTV startet, sieht er folgende Menüpunkte:
- Live TV
- Filme
- Serien
- Mediatheken

Beispiel-Ausgabe:
┌─────────────────────────┐
│   MultiTV               │
├─────────────────────────┤
│ ▶ Live TV              │
│ ▶ Filme                │
│ ▶ Serien               │
│ ▶ Mediatheken          │
└─────────────────────────┘
"""

# ==========================================
# 2. LIVE TV BEISPIEL
# ==========================================
"""
Wenn Benutzer auf "Live TV" klickt:

Kanäle werden aus beiden Quellen geladen:
- Sat.1 (Joyn + VIU)
- ProSieben (Joyn + VIU)
- Kabel Eins (Joyn + VIU)
- Sixx (Joyn + VIU)
- ran (Joyn)
- Energy (Joyn)
- ARD (VIU)
- ZDF (VIU)
- weitere Kanäle...

Die Liste ist alphabetisch sortiert und zeigt:
- Senderlogo
- Sendername
- Aktuelles Programm (wenn EPG aktiviert)

Der Benutzer sieht NICHT, ob der Stream von Joyn oder VIU kommt!
"""

# ==========================================
# 3. FILME BEISPIEL
# ==========================================
"""
Menü "Filme" zeigt:
├─ Top Filme
├─ Neu
└─ Nach Genre

Wenn "Top Filme" geklickt wird, zeigt das Addon:

[Poster-Wall View]
┌──────┐  ┌──────┐  ┌──────┐
│      │  │      │  │      │
│Poster│  │Poster│  │Poster│
│  1   │  │  2   │  │  3   │
│      │  │      │  │      │
└──────┘  └──────┘  └──────┘
Film 1    Film 2    Film 3
Rating: 8.5  Rating: 8.2  Rating: 7.9

Beim Fokus zeigt sich:
┌──────────────────────────────┐
│ Film 1                       │
│ Action, Drama | 2024         │
│ Rating: ★★★★★ (8.5)         │
│                              │
│ Ein absoluter Blockbuster... │
│ Mit Cast: Actor 1, Actor 2   │
│                              │
│ [PLAY] [INFO]                │
└──────────────────────────────┘
"""

# ==========================================
# 4. GENRE BEISPIEL
# ==========================================
"""
Filme → Nach Genre:
├─ Aktion
├─ Abenteuer
├─ Komödie
├─ Drama
├─ Fantasy
├─ Horror
├─ Romance
├─ Thriller
├─ Sport
├─ Dokumentation
└─ Animation

Wenn "Aktion" geklickt wird:
- 30-50 Aktionsfilme werden geladen
- Kombiniert aus VIU + Joyn
- Sortiert nach Relevanz/Rating
- Alle mit TMDB-Metadaten
"""

# ==========================================
# 5. SERIEN BEISPIEL
# ==========================================
"""
Serien → Top Serien:

Die Top Serien werden angezeigt mit:
- Serienposter
- Serie Name
- Anzahl Staffeln (z.B. "3 Staffeln")
- Rating
- Beschreibung
- Cast-Informationen

Beim Anklicken einer Serie:
→ Zeige Staffeln / Episoden
→ Streams aus VIU oder Joyn werden kombiniert
"""

# ==========================================
# 6. MEDIATHEKEN BEISPIEL
# ==========================================
"""
Mediatheken → ProSieben:

Dies zeigt alle Inhalte aus:
1. ProSieben (Joyn)
2. ProSieben (VIU)

→ Alles vermischt als eine Mediathek

Das Addon zeigt:
- Aktuelle Sendungen
- Verfügbare Episoden
- Archive
- Eventuelle Filme/Serien

Der Benutzer sieht NICHT die Unterscheidung der Quellen!
"""

# ==========================================
# 7. WIEDERGABE BEISPIEL
# ==========================================
"""
Wenn Benutzer auf einen Stream klickt:

1. Stream-URL wird ermittelt (von Joyn oder VIU)
2. TMDB-Metadaten werden zusammengestellt
3. Qualität wird gesetzt (Auto/720p/1080p)
4. Poster und Fanart werden geladen
5. Wiedergabe startet im Kodi-Player

Während Wiedergabe:
- Fortschritt wird gespeichert
- Qualität kann gewechselt werden
- Untitel (wenn verfügbar)
- Spulen vor/zurück möglich
"""

# ==========================================
# 8. FEHLERBEHANDLUNG BEISPIEL
# ==========================================
"""
Szenario: VIU nicht erreichbar

1. MultiTV versucht VIU zu kontaktieren
2. Timeout nach 10 Sekunden
3. Fallback auf Joyn
4. Wenn auch Joyn nicht antwortet:
   → Cache wird verwendet
5. Wenn kein Cache vorhanden:
   → Benachrichtigung: "Keine Inhalte verfügbar"

Das System ist robust - der Benutzer wird nicht mit Fehlern bombardiert!
"""

# ==========================================
# 9. CACHING BEISPIEL
# ==========================================
"""
Erste Anfrage:
1. MultiTV fragt VIU: "Gib mir Filme"
2. Antwortet in ~2-3 Sekunden
3. Daten werden mit Timestamp gespeichert
4. Benutzer sieht Ergebnis

Zweite Anfrage (innerhalb von 24 Stunden):
1. MultiTV prüft Cache
2. Findet Daten in: ~/.kodi/addon_data/plugin.video.multitv/cache/
3. Returned sofort (< 0.5 Sekunden)
4. Benutzer sieht blitzschnell das Ergebnis

Nach 24 Stunden:
1. Cache wird als abgelaufen markiert
2. Neue Anfrage an API
3. Frische Daten
"""

# ==========================================
# 10. SETTINGS BEISPIEL
# ==========================================
"""
Addon-Einstellungen:

┌────────────────────────────────────┐
│ MultiTV Einstellungen              │
├────────────────────────────────────┤
│ [Grundeinstellungen]               │
│                                    │
│ TMDB API Key:                      │
│ [_________________] <-- hier Key   │
│                                    │
│ Video-Qualität:                    │
│ ( ) Auto (x) 720p ( ) 1080p        │
│                                    │
│ [Erweiterte Einstellungen]         │
│                                    │
│ [✓] Joyn aktivieren                │
│ [✓] VIU aktivieren                 │
│ [✓] EPG aktivieren                 │
│ [✓] Debug-Logging                  │
│                                    │
│ Cache-TTL: 24 Stunden              │
│ [Cache löschen]                    │
└────────────────────────────────────┘
"""

# ==========================================
# CODE-BEISPIELE FÜR ENTWICKLER
# ==========================================

# Beispiel 1: Filme laden
from lib.api_viu import viu
from lib.api_joyn import joyn

movies_viu = viu.get_movies(category='trending', limit=20)
movies_joyn = joyn.get_movies(category='trending', limit=20)

all_movies = movies_viu + movies_joyn
all_movies.sort(key=lambda x: x.get('rating', 0), reverse=True)
print(f"Top 20 Filme: {len(all_movies)}")


# Beispiel 2: Cache-Nutzung
from lib.cache import cache

cache_key = "my_movies_top_20"
cached_data = cache.get(cache_key)

if cached_data:
    print("Daten aus Cache")
    movies = cached_data
else:
    print("Daten von API abrufen...")
    movies = all_movies
    cache.set(cache_key, movies)


# Beispiel 3: TMDB-Metadaten
from lib.tmdb import tmdb

search_result = tmdb.search_movie("Avengers")
if search_result and search_result['results']:
    movie = search_result['results'][0]
    metadata = tmdb.extract_metadata(movie, 'movie')
    print(f"Film: {metadata['title']}")
    print(f"Plot: {metadata['plot'][:100]}...")
    print(f"Poster: {metadata['poster']}")


# Beispiel 4: Navigation
from lib.navigation import navigation

top_films = navigation.get_movies_top()
print(f"Es gibt {len(top_films)} Top Filme")

for film in top_films[:5]:
    print(f"- {film['title']} ({film.get('rating', 'N/A')})")


# Beispiel 5: Player
from lib.player import player

list_items = [
    {
        'url': 'https://example.com/stream1.m3u8',
        'title': 'Film 1',
        'info': {'plot': 'Ein Film'},
        'thumbnail': 'https://example.com/poster1.jpg'
    },
    {
        'url': 'https://example.com/stream2.m3u8',
        'title': 'Film 2',
        'info': {'plot': 'Ein anderer Film'},
        'thumbnail': 'https://example.com/poster2.jpg'
    }
]

player.play_from_list(list_items[0]['url'], list_items[0]['title'])

---

Diese Beispiele zeigen, wie MultiTV in der Praxis funktioniert!
"""

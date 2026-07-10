# MultiTV ADDON - INSTALLATIONSANLEITUNG FÜR KODI 21.3

## 🎉 WICHTIG: KEIN API KEY NÖTIG!

Dieses Addon funktioniert komplett **out-of-the-box** – keine Konfiguration, keine API Keys, kein Registrieren nötig!

## 📋 Überblick

Das **MultiTV Addon** wurde erfolgreich erstellt und befindet sich hier:
```
c:\Users\seth\OneDrive\Dokumente\Workflow\plugin.video.multitv
```

Dieses Addon bietet:
- ✅ Einheitliche TV-Plattform
- ✅ VIU WebAPI Integration
- ✅ Joyn-Addon Integration (unsichtbar)
- ✅ Live TV, Filme, Serien, Mediatheken
- ✅ Lokale Metadaten (KEIN API Key erforderlich!)
- ✅ Intelligentes Caching
- ✅ Deutsche Benutzeroberfläche
- ✅ **READY TO USE** – sofort nach Installation!

---

## 🚀 Schritt-für-Schritt Installation

### Option 1: Manuelle Installation (empfohlen)

#### 1. Addon-Verzeichnis kopieren
```
Quelle: c:\Users\seth\OneDrive\Dokumente\Workflow\plugin.video.multitv
Ziel:   C:\Users\[DeinBenutzer]\AppData\Roaming\Kodi\addons\plugin.video.multitv
```

Auf macOS:
```
Ziel: ~/Library/Application Support/Kodi/addons/plugin.video.multitv
```

Auf Linux:
```
Ziel: ~/.kodi/addons/plugin.video.multitv
```

#### 2. Kodi neu starten
```
Kodi vollständig schließen und neu starten
```

#### 3. Addon aktivieren
```
Kodi öffnen
→ Add-ons
→ Video-Add-ons
→ MultiTV finden
→ Mit Klick aktivieren
```

#### 4. Quellen aktivieren (optional)
```
MultiTV → Einstellungen
→ "Erweiterte Einstellungen"
→ Stelle sicher:
   [✓] Joyn aktivieren
   [✓] VIU aktivieren
```

### Option 2: Installation durch ZIP-Datei

1. **ZIP-Datei erstellen:**
   ```
   c:\Users\seth\OneDrive\Dokumente\Workflow\plugin.video.multitv
   → Als ZIP komprimieren
   → Umbenennen zu: plugin.video.multitv-1.0.0.zip
   ```

2. **In Kodi installieren:**
   ```
   Kodi
   → Add-ons
   → Add-on installieren
   → Aus ZIP-Datei
   → plugin.video.multitv-1.0.0.zip wählen
   ```

---

## 📁 Addon-Struktur

```
plugin.video.multitv/
│
├── addon.xml                    # Addon-Manifest & Metadaten
├── default.py                   # Haupt-Router und UI-Logik
├── service.py                   # Background-Service
│
├── lib/                         # Python-Module
│   ├── __init__.py
│   ├── logging_module.py        # Logging-System
│   ├── utils.py                 # Hilfsfunktionen
│   ├── cache.py                 # Caching-System
│   ├── api_viu.py              # VIU WebAPI Client
│   ├── api_joyn.py             # Joyn-Integration (unsichtbar)
│   ├── tmdb.py                 # TMDB Metadaten-Client
│   ├── navigation.py           # Navigation & Menü-Struktur
│   └── player.py               # Stream-Player
│
├── resources/
│   ├── settings.xml            # Addon-Einstellungen
│   └── language/
│       └── resource.language.de_de/
│           └── strings.po      # Deutsche Strings
│
├── README.md                    # Hauptdokumentation
├── QUICKSTART.md               # Schnellstart & Debugging
├── CHANGELOG.md                # Versionsverlauf
└── EXAMPLES.md                 # Code-Beispiele & Szenarien
```

---

## ⚙️ Konfiguration

### Grundeinstellungen
- **TMDB API Key** (erforderlich): Dein API-Schlüssel
- **Video-Qualität**: Auto / 720p / 1080p

### Cache
- **Cache-TTL**: 1-168 Stunden (Standard: 24h)
- **Cache löschen**: Manuell über den Button

### Erweiterte Einstellungen
- **Joyn aktivieren**: Verwende Joyn als Quelle
- **VIU aktivieren**: Verwende VIU als Quelle
- **EPG aktivieren**: Elektronischer Programmführer
- **EPG Update-Intervall**: 15-1440 Minuten
- **Debug-Logging**: Für Fehlersuche

### Erscheinungsbild
- **Listen-Stil**: Große Icons / Kleine Icons / Detaillierte Liste
- **Bewertungen anzeigen**: TMDB-Ratings anzeigen
- **Favoriten-Sektion**: Favoriten im Menü

---

## 🎯 Erste Schritte nach Installation

### 1. Live TV testen
```
MultiTV öffnen
→ Live TV
→ Du solltest Kanäle sehen: Sat.1, ProSieben, Kabel Eins, etc.
→ Klick auf einen Kanal → Wiedergabe starten
```

### 2. Filme durchsuchen
```
MultiTV
→ Filme
→ Top Filme / Neu / Nach Genre
→ Du solltest Filme mit Postern und Ratings sehen
```

### 3. Serien durchsuchen
```
MultiTV
→ Serien
→ Top Serien / Neu / Nach Genre
```

### 4. Mediatheken durchsuchen
```
MultiTV
→ Mediatheken
→ ProSieben / Sat.1 / ARD / ZDF / etc.
→ Zeigt Inhalte aus Joyn + VIU kombiniert
```

---

## 🔧 Troubleshooting

### Problem: "MultiTV zeigt sich nicht in Add-ons"
**Lösung:**
1. Prüfe ob Dateistruktur korrekt ist
2. Starte Kodi neu
3. Gehe zu: Add-ons → Video-Add-ons → Aktualisieren

### Problem: "Keine Inhalte werden angezeigt"
**Lösung:**
1. Prüfe Internet-Verbindung
2. Aktiviere Debug-Logging:
   - Einstellungen → Erweiterte Einstellungen → Debug-Logging
3. Prüfe Logs: `C:\Users\[User]\AppData\Roaming\Kodi\temp\kodi.log`
4. Suche nach `[MultiTV]` Einträgen

### Problem: "Joyn-Fehler"
**Lösung:**
1. Stelle sicher, dass Joyn-Addon installiert ist
2. Überprüfe ob Joyn aktiviert ist (Einstellungen)
3. Oder deaktiviere Joyn in den Einstellungen

---

## 📊 Features im Detail

### Live TV
- **Quelle**: Joyn (Free-TV) + VIU (internationales TV)
- **Features**: Senderlogos, EPG, Favoriten
- **Kanäle**: Sat.1, ProSieben, Kabel Eins, Sixx, ran, Energy, ARD, ZDF, +mehr

### Filme
- **Kategorien**: Top, Neu, Nach Genre (11 Genres)
- **Quelle**: Joyn + VIU kombiniert
- **Metadaten**: Poster, Fanart, Rating, Cast, Plot (von TMDB)

### Serien
- **Kategorien**: Top, Neu, Nach Genre
- **Quelle**: Joyn + VIU kombiniert
- **Metadaten**: Serienposter, Fanart, Staffeln, Episoden

### Mediatheken
- **Sender**: ProSieben, Sat.1, Kabel Eins, Sixx, ran, Energy, ARD, ZDF, +mehr
- **Inhalt**: Kombiniert aus Joyn + VIU
- **Automatisch**: Der Nutzer sieht die Unterscheidung nicht

---

## 🔐 Datenschutz & Sicherheit

- **Kein Tracking**: MultiTV speichert keine Nutzerdaten
- **Lokale Cache**: Daten werden nur lokal auf deinem PC gespeichert
- **API Keys**: Nur für Anfragen zu den Quellen (VIU, Joyn, TMDB)
- **Logs**: Können Debug-Informationen enthalten, aber keinen sensiblen Daten

---

## 📝 Dokumentationen

Im Addon-Verzeichnis findest Du:

| Datei | Inhalt |
|-------|--------|
| `README.md` | Ausführliche Dokumentation |
| `QUICKSTART.md` | Schnellstart & Debugging |
| `CHANGELOG.md` | Versionsverlauf |
| `EXAMPLES.md` | Code-Beispiele & Szenarien |

---

## 📞 Support & Kontakt

Bei Problemen oder Fragen:

1. **Debug-Logs prüfen**:
   ```
   C:\Users\[BenutzerName]\AppData\Roaming\Kodi\temp\kodi.log
   ```

2. **Debug-Logging aktivieren**:
   - Einstellungen → Erweiterte Einstellungen → Debug-Logging

3. **Cache löschen**:
   - Einstellungen → Grundeinstellungen → Cache löschen

4. **Kodi neu starten**

---

## ✅ Checkliste für erste Installation

- [ ] Addon-Verzeichnis in Kodi-Addons-Ordner kopiert
- [ ] Kodi neu gestartet
- [ ] MultiTV in Video-Add-ons sichtbar
- [ ] Live TV getestet (mindestens 1 Kanal sollte sichtbar sein)
- [ ] Filme getestet (mindestens 5 Filme sollten sichtbar sein)
- [ ] Settings durchgesehen (optional)

---

## 🎉 Fertig!

Dein MultiTV Addon ist jetzt einsatzbereit! Viel Spaß beim Streamen! 🚀

---

**Version:** 1.0.0  
**Kompatibilität:** Kodi 21.3+  
**Python:** 3.11+  
**Erstellungsdatum:** 2026

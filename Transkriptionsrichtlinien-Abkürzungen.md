---
title: Transkriptionsrichtlinien
output: word_document
---

Am Beginn jeder Datei wird notiert:

```
TEXT: PTA-ID (sc. pta0001.pta001)
HS: Ort_Bibliothek_Sammlung_Nr
SIGLE: Sigle
DIKTYON: Diktyon-ID
EDITOR: Name (Kürzel)
DATUM: Datum der Transkription im Format 2022-01-01
```

Weitere, mögliche Angaben im Kopf der Transkription (werden vom Script nicht verwendet):

```
PDF: S. Seitenzahl in PDF
SCAN: URL
```

# Titel/Lemma

Wird mit `0Lemma/Titel0` ausgezeichnet. **Muss** angegeben werden, ggfs. leer lassen (sc. `0 0`)

# Umbrüche

Umbrüche werden jeweils am Ende der Zeile angegeben.

- Zeilenumbruch: `/` (Griechische Tastatur: -Leerzeichen) (Leerzeichen davor und danach, im Wort ohne Leerzeichen davor oder danach)
- Spaltenumbruch: `//` (Leerzeichen davor und danach, im Wort ohne Leerzeichen davor oder danach)
- Seitenumbruch: `///(Folioangabe)` (Leerzeichen davor und danach, im Wort ohne Leerzeichen davor oder danach)

Die erste Seite der Transkription wird mit `(Folionr+r/v)` am Beginn der Transkription angegeben (sc. `(112r)`).

# Zeichensetzung

Wird – ohne explizite Auszeichnung – wie in der Handschrift angegeben. (Hochpunkt: Shift AltGr +)

# Initialen und Ektheseis

- Initialen: `1Buchstabe1`
- Ektheseis: `2Buchstabe2`

# Absätze

Absätze werden durch eine leere Zeile markiert.

# Besondere Texte

- Marginalien: `3Text~Position:1=oben/2=unten/3=innen/4=außen~3` (~: Griechische Tastatur = ^Leerzeichen)
- getilgter Text: `4TextTextText~1=Rasur/2=durchgestrichen/3=expungiert~4`
- Korrektur: `4ersetzter Text~0=Verweiszeichen/1=Rasur/2=durchgestrichen/3=expungiert/4=ohne Zeichen/5=unterstrichen~korrigierender Text~Position:1=über der Zeile/2=in der Zeile/3=Rand~4`
- hinzugefügter Text (ohne Korrektur): `5hinzugefügter Text~Position:1=über der Zeile/2=in der Zeile/3=Rand~5`
- Lücke im Text: `6...geschätzte Anzahl der Buchstaben...6`
- Nicht lesbarer Text: `7...Anzahl der Buchstaben...7`
- Unsichere Lesung: `8gelesener Text8`
- Nomina sacra: `9Abkürzung~Auflösung9`
- Zahlen: `10Zahl(Buchstaben)10`

# Zitate

In der Handschrift mit Diple markierte Zitate werden durch `@ `, ggfs. doppelt, (Griechische Tastatur: `:`) *und folgendem Leerzeichen* am Beginn der jeweiligen Zeile markiert.

# Paragraphos

In der Handschrift mit Paragraphos am Rand markierte Zeilen werden durch `--` *und folgendem Leerzeichen* am Beginn der jeweiligen Zeile markiert.

# Vyk ruokalista discord botti v1.2

# Tämä repo on kopioitu yksityisestä reposta. Ainoa muutos on yksityisen tiedon piiloittaminen, kuten discord botin tokeni.

## Asennus

Salli asennustiedostojen suorittaminen nykyisellä käyttäjällä.
```bash
chmod u+x setup.sh setup_systemd.sh tools/generate_regs.sh
```

Suorita asennusohjelma. Skripti luo pythonille virtuaali ympäristön ja asentaa tarvittavat python riippuvuudet.
Sen jälkeen se pyytää tarvittavat discord tokenit, mikäli config.py tiedostoa ei ole olemassa.
Skripti käyttää systemd ajastimia toimiakseen.
```bash
./setup.sh
```

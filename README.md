# Väsymislaskenta ohjelma lujuuslaskentaan

Sovelluksella voi laskea niin kutsutun varmuuskertoimen jännityshistorian perusteella. Jännityshistoria voi olla laskettu esimerkiksi elementtimenetelmällä tai mitattu.

## Python versio 3.10.0

Toiminta testattu vain Python versiolla 3.10.0

## Ohjelman kehitysympäristö on Windows 10

Python3 komennot on korvattu python komennoilla

## Dokumentaatio

- [Käyttöohje](./dokumentaatio/kayttoohje.md)
- [Vaatimusmäärittely](./dokumentaatio/vaatimusmaarittely.md)
- [Arkkitehtuurikuvaus](./dokumentaatio/arkkitehtuuri.md)
- [Testausdokumentti](./dokumentaatio/testaus.md)
- [Työaikakirjanpito](./dokumentaatio/tuntikirjanpito.md)

## Asennus

1. Asenna riippuvuudet komennolla:

```bash
poetry install
```

2. Suorita vaadittavat alustustoimenpiteet komennolla:

```bash
poetry run invoke build
```

3. Käynnistä sovellus komennolla:

```bash
poetry run invoke start
```

## Komentorivitoiminnot

### Ohjelman suorittaminen

Ohjelman pystyy suorittamaan komennolla:


```bash
poetry run invoke start
```

### Testaus

Testit suoritetaan komennolla:

```bash
poetry run invoke test
```

### Testikattavuus

Testikattavuusraportin voi generoida komennolla:

```bash
poetry run invoke coverage-report
```

Raportti generoituu _htmlcov_-hakemistoon.

### Pylint

Tiedoston [.pylintrc](./.pylintrc) määrittelemät tarkistukset voi suorittaa komennolla:

```bash
poetry run invoke lint
```

<!--
## Viikko 1

[gitlog.txt](https://github.com/ivaeisaenen/ot-harjoitustyo/blob/master/laskarit/viikko1/gitlog.txt)

[komentorivi.txt](https://github.com/ivaeisaenen/ot-harjoitustyo/blob/master/laskarit/viikko1/komentorivi.txt)

## Viikko 2

[unicafe_test_coverage.png](https://github.com/ivaeisaenen/ot-harjoitustyo/blob/master/laskarit/viikko2/unicafe_test_coverage_screenshot.PNG)

[vaatimusten määrittely dokumentti](https://github.com/ivaeisaenen/ot-harjoitustyo/blob/master/dokumentaatio/vaatimustenmaarittely.md)

[Tuntikirjapito]((https://github.com/ivaeisaenen/ot-harjoitustyo/blob/master/dokumentaatio/tuntikirjanpito.md)

## Viikko 3

[src](https://github.com/ivaeisaenen/ot-harjoitustyo/blob/master/src)
-->
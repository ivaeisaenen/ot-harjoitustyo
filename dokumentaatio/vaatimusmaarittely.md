# Vaatimusmäärittely

## Sovelluksen tarkoitus

Soveluksen avulla käyttäjän on mahdollista laskea lähtötietojen perusteella varmuuskertoimia tai elinikiä haluttujen kriteereiden perusteella
## Käyttäjät

Kaikki käyttäjät ovat normaaleja käyttäjiä, ei ole tarvetta ylläpito tunnuksille.

## Käyttöliittymäluonnos

Sovelluksen pääalueet on:
- Lähtötietojen valinta jännityshistorian osalta (ASCII tiedosto)
- Kriteerin valinta
- Materiaalidatan syöttö/valinta

Alustava idea on että käyttäjän valinnat muodostavat dict muotoisen tietorakenteen joka voidaan myös tallentaa lähtötiedoksi. Voi käyttää siis graafiesesti tai komentoriviltä.

## Perusversion tarjoama toiminnallisuus

- Käyttäjä valitsee ASCII tiedoston missä on haluttu jännityshistoria
  - mahdollisesti lisä optiona HDF5 tai eri muotoiset ASCII tiedostot

- Käyttäjä valitsee käytettävän kriteerin esimerkiksi Von Mises tai Manson–McKnight tai Findley

- Käyttäjä valitsee materiaaliparametrit ainakin väsymisraja ja väsymisraja tykyttävällä kuormalla
	- Mahdollisesti lisää parametereja riippuen kriteereistä

- Käyttäjä saa lyhyen raportin tuloksista ja tulokset kirjataan ASCII tiedostoon

## Jatkokehitysideoita

Perusversion jälkeen järjestelmää täydennetään ajan salliessa esim. seuraavilla toiminnallisuuksilla

- Lisää erilaisia kriteereitä
- Mahdollisuus muodostaa eri tavoin uusia materiaaleja
- Mahdollisuus erimuotoisiin tulosteisiin
- Mahdollisuus valita erilaisia tuloksia
- Lähtötietoja voi ladata ja tallentaa

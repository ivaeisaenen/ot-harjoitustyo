# Vaatimusmäärittely

## Sovelluksen tarkoitus

Soveluksen avulla käyttäjän on mahdollista laskea lähtötietojen perusteella varmuuskertoimia haluttujen kriteereiden ja keskijännityskorjausten perusteella

## Käyttäjät

Kaikki käyttäjät ovat normaaleja käyttäjiä, ei ole tarvetta ylläpito tunnuksille.

## Käyttöliittymäluonnos

Sovelluksen pääalueet on:
- Lähtötietojen valinta jännityshistorian osalta (ASCII tiedosto)
- Kriteerin valinta (json)
- Materiaalidatan syöttö/valinta (json)

Alustava idea on että käyttäjän valinnat muodostavat dict muotoisen tietorakenteen joka voidaan myös tallentaa lähtötiedoksi. Voi käyttää siis graafiesesti tai komentoriviltä, mutta toistaiseksi graafinen käyttöliittymä millä lähtötiedosto luodaan on optio.

Tällä sovelluslogiikalla tämä ohjelma voidaan kykeä helposti osaksi jotain elementtimenetelmän laskentaohjelmaa jossa voidaan suorittaa python sciptejä. Pythonscripti käynnistää tämän ohjelman joka laskee tulokset ja ilmoittaa kun ne ovat valmiit ja voidaan ladata elementtimenetelmä ohjelmaan tarkastelua varten. Myös graafisen käyttöliittymän voi toteuttaa täysin erillisenä.

## Perusversion tarjoama toiminnallisuus

- Käyttäjä valitsee ASCII tiedoston missä on haluttu jännityshistoria
  - Tällä hetkellä jännitystensori niin sanotussa Voigtin esitysmuodossa (löytyy Wikipediasta)
  - Mahdollisesti loptiona HDF5 tai eri muotoiset ASCII tiedostot

- Käyttäjä valitsee käytettävän kriteerin esimerkiksi Von Mises tai Manson–McKnight tai Findley
  - Tämän kurssin rajoissa toteutuetaan vain kaikkein yksinkertaisin kriteeri Von Mises

- Käyttäjä valitsee materiaaliparametrit ainakin väsymisraja ja väsymisraja tykyttävällä kuormalla
	- Mahdollisesti lisää parametereja riippuen kriteereistä

- Tulokset kirjataan ASCII tiedostoon
  - Optiona olisi tehdä lyhyt ascii raportti tuloksista ja muutama plotti matplotlib.pyplot modulin avulla

## Jatkokehitysideoita

Perusversion jälkeen järjestelmää täydennetään ajan salliessa esim. seuraavilla toiminnallisuuksilla

- Lisää erilaisia kriteereitä ja keskijännätyskorjauksia
- Mahdollisuus laskea varmuuskertoimen lisäksi elinikiä
- Mahdollisuus muodostaa eri tavoin uusia materiaaleja
- Mahdollisuus erimuotoisiin tulosteisiin
- Mahdollisuus valita erilaisia tuloksia
- Lähtötietoja voi ladata ja tallentaa
- Automaattiraportteja

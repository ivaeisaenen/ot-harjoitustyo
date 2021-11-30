# Arkkitehtuurikuvaus

Ohjelman tarkoitus on laskea varmuuskertoimia jännityshistoria perusteella. 

Ohjelman syötteitä ovat:

- Jännityshistoria (Luetaan tiedostosta)

- Materiaalitiedot (tällä hetkellä dict index.py tiedostossa, luetaan myöhemmin tiedostosta)

Varsinaisessa laskennassa valitaan:

- Keskijännityskorjaus (esimerkiksi Goodman tai vastaava)
- Vauriokriteeri (Esimrkiksi Von Mises, MMK, Findley, Matake ja niin edelleen)

Tulos kirjoitetaan tulostiedostoon ja sisältää tuloksen jokaiselle yksittäisen jännityshistorian yksikölle

![Arkkitehtuuri](./kuvat/arkkitehtuuri.png)

## Rakenne

Tarkoitus on erottaa ohjelmistologiikka, käyttöliittymä ja varsinaisen laskennan suorittavat modulit täysin toisistaan.

Käyttöliittymä ja ohjelmansuoritus ovat yhteydessä json tiedostoilla jossa on käyttöliittymän kautta syötetyt tiedot joilla ohjelma voidaan suorittaa.

## Käyttöliittymä

Ohjelmaa käytettäisiin tosielämässä osana automatisoitua prosessia eikä graafista käyttöliittymää tarvita mihinkään. Tosielämässä laskenta olisi myös erittäin raskasta ja se suoritettaisiin laskenta clusterilla.

Ohjelman syötteen voi kuitenkin helposti paitsi kirjoittaa käsin tiedostoon muodostaa myös myöhemmin kehitettävän käyttöliittymän kautta.

## Sovelluslogiikka

* 1. Lähtötiedot luodaan joko kästin tai mahdollisen GUI kautta

* 2. Ohjelma ajetaan lähtötietojen perusteella
	* 2.1 Luetaan jännityshistoria
	* 2.2 Lasketaan ekvivalentti jännitys
	* 2.3 lasketaan varmuuskerroin ja muut tulokset

* 3. Kirjoitetaan tulokset

Sovellukset suoritus on varsin suoraviivaista.
* 1. päämodulia index aletaan suorittaa jolloin luetaan lähtötiedot
	* 1.1 materials.json
	* 1.2 inputs.json
	* 1.3 lähtötiedoissa määritellyt jännityshistoria tiedostot käyttämällä tools modulin read_stress funktiota
* 2. suoritetaan modulin tools calculate funktio hakee moduleista criteria ja mean_stress_correction lähtötietoja vastaavat funktiot ja suoritus alkaa
	* 2.1 aloitetaan criteria modulin mukainen varmuuskertoimen laskenta jossa jokaiselle solmulle
		* 2.1.1 lasketaan equivalentti jännitys ensiksi muodostamalla yksiaksiaalinen jännitys ja sitten sen perusteella etsimällä historian yli amplitudi- ja keskijännitys
		* 2.1.2 suoritetaan keskijännityskorjaus 
		* 2.1.3 lasketaan varmuuskerroin ja palautetaan varmuuskerroin ja muut tulokset
* 3. modulissa index kirjoitetaan modulin tools funktiolla write_results tulokset tiedostoon

Tämän jälkeen tuloksia voi tarkastella visuaalisesti vaikkapa paraviewillä kunhan solmuihin liittyvät koordinaatit ovat myös saatavilla

![Sekvenssi](./kuvat/sekvenssi.png)

### Tiedostot


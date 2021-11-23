# Arkkitehtuurikuvaus

Ohjelman tarkoitus on laskea varmuuskertoimia jännityshistoria perusteella. 

Ohjelman syötteitä ovat:

- Jännityshistoria (Luetaan tiedostosta)

- Materiaalitiedot (tällä hetkellä dict index.py tiedostossa, luetaan myöhemmin tiedostosta)

Varsinaisessa laskennassa valitaan:

- Keskijännityskorjaus (esimerkiksi Goodman tai vastaava)
- Vauriokriteeri (Esimrkiksi Von Mises, MMK, Findley, Matake ja niin edelleen)

Tulos kirjoitetaan tulostiedostoon ja sisältää tuloksen jokaiselle yksittäisen jännityshistorian yksikölle

## Rakenne

Tarkoitus on erottaa ohjelmistologiikka, käyttöliittymä ja varsinaisen laskennan suorittavat modulit täysin toisistaan.

## Käyttöliittymä

Ohjelmaa käytettäisiin tosielämässä osana automatisoitua prosessia eikä graafista käyttöliittymää tarvita mihinkään. Tosielämässä laskenta olisi myös erittäin raskasta ja se suoritettaisiin laskenta clusterilla.

Ohjelman syötteen voi kuitenkin helposti paitsi kirjoittaa käsin tiedostoon muodostaa myös myöhemmin kehitettävän käyttöliittymän kautta.

## Sovelluslogiikka

1. Lähtötiedot luodaan joko kästin tai mahdollisen GUI kautta

2. Ohjelma ajetaan lähtötietojen perusteella
	2.1 Luetaan jännityshistoria
	2.2 Lasketaan ekvivalentti jännitys
	2.3 lasketaan varmuuskerroin ja muut tulokset


3. Tarkastellaan tuloksia

### Tiedostot
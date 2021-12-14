# Testaus

## test_mean_stress_correction

Testaa keksijännityskorjauksia

## test_criteria

Testaa Von Mises kriteeriä

# test_tools

Testaa toolscalculate() funktiota joka käytännössä ajaa koko laskennan lukuunottamatta input/output lukemisia.

# test_inpout

Testaa input/output modulia inpout.py. Tarvittavat tiedostot ovat tällä hetkellä data/ hakemistossa. Samoja tiedostoja käytetään kun ohjelma ajetaan, koska ohjeissa on että ohjelmaa täytyy pystyä ajamaan start komennolla niin nämä tiedostot on joka tapauksessa sisällytettävä.


## Systeemitestaus

Yhden systeemitestauksen voi suorittaa ajamalla index.py oletusarvoilla ja .data kansion oletustiedostoilla. Tälle tulostiedostolle ei ole vielä tarkistusta mutta logi ja tulostiedostoista näkee kyllä toimiiko ohjelma ylipäätänsä.
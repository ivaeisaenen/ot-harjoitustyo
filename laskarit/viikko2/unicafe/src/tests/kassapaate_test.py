import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
    
    def test_luotu_kassapaate_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)
    
    def test_syo_edullisesti_kateisella_tasaraha(self):
        maksu = 240
        rahaa_takaisin = self.kassapaate.syo_edullisesti_kateisella(maksu)
        self.assertEqual(rahaa_takaisin, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000+maksu)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_syo_edullisesti_kateisella_yliraha(self):
        maksu = 500
        hinta = 240
        rahaa_takaisin = self.kassapaate.syo_edullisesti_kateisella(maksu)
        self.assertEqual(rahaa_takaisin, maksu-hinta)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000+hinta)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_syo_edullisesti_kateisella_aliraha(self):
        maksu = 200
        hinta = 240
        rahaa_takaisin = self.kassapaate.syo_edullisesti_kateisella(maksu)
        self.assertEqual(rahaa_takaisin, maksu)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_syo_maukkaasti_kateisella_tasaraha(self):
        maksu = 400
        rahaa_takaisin = self.kassapaate.syo_maukkaasti_kateisella(maksu)
        self.assertEqual(rahaa_takaisin, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000+maksu)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_syo_maukkaasti_kateisella_yliraha(self):
        maksu = 500
        hinta = 400
        rahaa_takaisin = self.kassapaate.syo_maukkaasti_kateisella(maksu)
        self.assertEqual(rahaa_takaisin, maksu-hinta)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000+hinta)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_syo_maukkaasti_kateisella_aliraha(self):
        maksu = 200
        hinta = 400
        rahaa_takaisin = self.kassapaate.syo_maukkaasti_kateisella(maksu)
        self.assertEqual(rahaa_takaisin, maksu)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)
    
    def test_syo_edullisesti_kortilla_kun_kortilla_on_tarpeeksi_rahaa(self):
        maksu = 500
        kortti = Maksukortti(maksu)
        tapahtuma = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(tapahtuma, True)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.maukkaat, 0)    

    def test_syo_edullisesti_kortilla_kun_kortilla_ei_ole_tarpeeksi_rahaa(self):
        maksu = 200
        kortti = Maksukortti(maksu)
        tapahtuma = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(tapahtuma, False)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_syo_maukkaasti_kortilla_kun_kortilla_on_tarpeeksi_rahaa(self):
        maksu = 500
        kortti = Maksukortti(maksu)
        tapahtuma = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(tapahtuma, True)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 1)    

    def test_syo_maukkaasti_kortilla_kun_kortilla_ei_ole_tarpeeksi_rahaa(self):
        maksu = 200
        kortti = Maksukortti(maksu)
        tapahtuma = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(tapahtuma, False)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        
    def test_lataa_rahaa_kortille_postiiivinen_summa(self):
        alku = 100
        summa = 200
        kortti = Maksukortti(alku)
        self.kassapaate.lataa_rahaa_kortille(kortti, summa)
        self.assertEqual(kortti.saldo, alku+summa)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000+summa)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_lataa_rahaa_kortille_negatiivinen_summa(self):
        alku = 100
        summa = -200
        kortti = Maksukortti(alku)
        self.kassapaate.lataa_rahaa_kortille(kortti, summa)
        self.assertEqual(kortti.saldo, alku)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)
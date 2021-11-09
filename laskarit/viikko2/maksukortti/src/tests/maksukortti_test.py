import unittest
from maksukortti import Maksukortti


class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.kortti = Maksukortti(10)

    def test_konstruktori_asettaa_saldon_oikein(self):
        self.assertEqual(str(self.kortti), "Kortilla on rahaa 10 euroa")

    def test_syo_edullisesti_vahentaa_saldoa_oikein(self):
        self.kortti.syo_edullisesti()
        self.assertEqual(str(self.kortti), "Kortilla on rahaa 7.5 euroa")

    def test_syo_maukkaasti_vahentaa_saldoa_oikein(self):
        self.kortti.syo_maukkaasti()
        self.assertEqual(str(self.kortti), "Kortilla on rahaa 6 euroa")

    def test_syo_edullisesti_ei_vie_saldoa_negatiiviseksi(self):
        self.kortti.syo_maukkaasti()
        self.kortti.syo_maukkaasti()
        self.kortti.syo_edullisesti()
        self.assertEqual("Kortilla on rahaa 2 euroa", str(self.kortti))

    def test_kortille_voi_ladata_rahaa(self):
        self.kortti.lataa_rahaa(25)
        self.assertEqual(str(self.kortti), "Kortilla on rahaa 35 euroa")

    def test_kortin_saldo_ei_ylita_maksimiarvoa(self):
        self.kortti.lataa_rahaa(200)
        self.assertEqual(str(self.kortti), "Kortilla on rahaa 150 euroa")

    def test_negatiivisen_summan_lataaminen_ei_muuta_kotin_saldoa(self):
        self.kortti.lataa_rahaa(-100)
        self.assertEqual(str(self.kortti), "Kortilla on rahaa 10 euroa")

    def test_kortilla_pystyy_ostamaan_edullisen_lounaan_niukalla_saldolla(self):
        kortti = Maksukortti(2.5)
        kortti.syo_edullisesti()
        self.assertEqual(str(kortti), "Kortilla on rahaa 0.0 euroa")

    def test_kortilla_pystyy_ostamaan_maukkaan_lounaan_niukalla_saldolla(self):
        kortti = Maksukortti(4)
        kortti.syo_maukkaasti()
        self.assertEqual(str(kortti), "Kortilla on rahaa 0 euroa")


# class TestMaksukortti(unittest.TestCase):
    # def setUp(self):
        # print("Set up goes here")

    # def test_konstruktori_asettaa_saldon_oikein(self):
        # kortti = Maksukortti(10)
        # vastaus = str(kortti)
        # self.assertEqual(vastaus, "Kortilla on rahaa 10 euroa")

# #    def test_konstruktori_asettaa_saldon_oikein(self):
# #        kortti = Maksukortti(10)
# #        self.assertEqual(str(kortti), "Kortilla on rahaa 10 euroa")

    # def test_syo_edullisesti_vahentaa_saldoa_oikein(self):
        # kortti = Maksukortti(10)
        # kortti.syo_edullisesti()
        # self.assertEqual(str(kortti), "Kortilla on rahaa 7.5 euroa")

    # def test_syo_maukkaasti_vahentaa_saldoa_oikein(self):
        # kortti = Maksukortti(10)
        # kortti.syo_maukkaasti()
        # self.assertEqual(str(kortti), "Kortilla on rahaa 6 euroa")

    # def test_syo_edullisesti_ei_vie_saldoa_negatiiviseksi(self):
        # kortti = Maksukortti(10)
        # kortti.syo_maukkaasti()
        # kortti.syo_maukkaasti()
        # # nyt kortin saldo on 2
        # self.assertEqual(str(kortti), "Kortilla on rahaa 2 euroa")

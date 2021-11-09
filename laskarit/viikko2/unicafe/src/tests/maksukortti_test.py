import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(10)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

#    def test_konstruktori_asettaa_saldon_oikein(self):
#        self.assertEqual(str(self.kortti), "Kortilla on rahaa 10 euroa")
        
    def test_kortin_saldo_alussa_oikein(self):
        self.assertEqual(self.maksukortti.saldo, 10)

    def test_rahan_lataaminen_kasvattaa_saldoa(self):
        self.maksukortti.lataa_rahaa(100)
        self.assertEqual(self.maksukortti.saldo, 110)

    def test_saldo_vahenee_jos_tarpeeksi_rahaa(self):
        palaute = self.maksukortti.ota_rahaa(9)
        self.assertEqual(self.maksukortti.saldo, 1)
        self.assertEqual(palaute, True)

    def test_saldo_ei_muutu_jos_liian_vahan_rahaa(self):
        palaute = self.maksukortti.ota_rahaa(11)
        self.assertEqual(self.maksukortti.saldo, 10)
        self.assertEqual(palaute, False)
    
    def test_print(self):
        self.assertEqual(self.maksukortti.__str__(), "saldo: 0.1")
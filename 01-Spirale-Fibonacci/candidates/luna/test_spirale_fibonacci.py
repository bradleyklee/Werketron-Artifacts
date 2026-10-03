import importlib.util
import pathlib
import subprocess
import sys
import unittest


PROGRAMMA = pathlib.Path(__file__).with_name("spirale_fibonacci.py")
SPEC = importlib.util.spec_from_file_location("spirale_fibonacci", PROGRAMMA)
spirale = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = spirale
SPEC.loader.exec_module(spirale)


class TestSpiraleFibonacci(unittest.TestCase):
    def test_verifica_per_valori_crescenti(self):
        for n in range(2, 16):
            with self.subTest(n=n):
                self.assertTrue(spirale.verifica(n))

    def test_interfaccia_verifica(self):
        risultato = subprocess.run(
            [sys.executable, str(PROGRAMMA), "12", "--verifica"],
            check=True, capture_output=True, text=True,
        )
        self.assertIn("N=12", risultato.stdout)
        self.assertEqual(risultato.stderr, "")

    def test_tela_braille_e_griglia_ascii(self):
        tela = subprocess.run(
            [sys.executable, str(PROGRAMMA), "5"],
            check=True, capture_output=True, text=True,
        ).stdout
        self.assertTrue(all("\u2800" <= carattere <= "\u28ff"
                            for carattere in tela if carattere != "\n"))
        righe = tela.splitlines()
        self.assertTrue(all(len(riga) == len(righe[0]) for riga in righe))
        self.assertTrue(all(any(riga[colonna] != "\u2800" for riga in righe)
                            for colonna in range(len(righe[0]))))
        self.assertTrue(all(any(carattere != "\u2800" for carattere in riga)
                            for riga in righe))
        griglia = subprocess.run(
            [sys.executable, str(PROGRAMMA), "5", "--griglia"],
            check=True, capture_output=True, text=True,
        ).stdout
        self.assertTrue(all(ord(carattere) < 128 for carattere in griglia))

    def test_rifiuta_n_invalido(self):
        risultato = subprocess.run(
            [sys.executable, str(PROGRAMMA), "1"],
            capture_output=True, text=True,
        )
        self.assertNotEqual(risultato.returncode, 0)
        self.assertIn("N deve essere almeno 2", risultato.stderr)

    def test_aiuto_in_italiano(self):
        risultato = subprocess.run(
            [sys.executable, str(PROGRAMMA), "--aiuto"],
            check=True, capture_output=True, text=True,
        )
        self.assertIn("Uso:", risultato.stdout)
        self.assertEqual(risultato.stderr, "")


if __name__ == "__main__":
    unittest.main()

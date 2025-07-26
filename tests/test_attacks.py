import unittest
import os
import zipfile
import pyzipper
from src.core.attacks import DictionaryAttack, BruteForceAttack

class TestAttacks(unittest.TestCase):

    def setUp(self):
        # Create a dummy ZIP file with a known password
        self.zip_path = "test.zip"
        self.password = "1234"
        with pyzipper.AESZipFile(self.zip_path, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
            zf.setpassword(self.password.encode())
            zf.writestr("test_file.txt", "This is a test file.")

        # Create a dummy dictionary file
        self.dict_path = "test_dict.txt"
        with open(self.dict_path, "w") as f:
            f.write("password\n")
            f.write("12345\n")
            f.write("1234\n")
            f.write("test\n")

    def tearDown(self):
        # Clean up the dummy files
        if os.path.exists(self.zip_path):
            os.remove(self.zip_path)
        if os.path.exists(self.dict_path):
            os.remove(self.dict_path)

    def test_dictionary_attack_success(self):
        attack = DictionaryAttack(self.zip_path, self.dict_path)
        found_password = attack.run()
        self.assertEqual(found_password, self.password)

    def test_dictionary_attack_fail(self):
        # Create a dictionary without the correct password
        dict_path = "test_dict_fail.txt"
        with open(dict_path, "w") as f:
            f.write("password\n")
            f.write("12345\n")
            f.write("test\n")

        attack = DictionaryAttack(self.zip_path, dict_path)
        found_password = attack.run()
        self.assertIsNone(found_password)
        os.remove(dict_path)

    def test_brute_force_attack_success(self):
        attack = BruteForceAttack(self.zip_path, length=4, numbers=True, letters=False, symbols=False)
        found_password = attack.run()
        self.assertEqual(found_password, self.password)

    def test_brute_force_attack_fail(self):
        # Test with a length that is too short
        attack = BruteForceAttack(self.zip_path, length=3, numbers=True, letters=False, symbols=False)
        found_password = attack.run()
        self.assertIsNone(found_password)

if __name__ == "__main__":
    unittest.main()

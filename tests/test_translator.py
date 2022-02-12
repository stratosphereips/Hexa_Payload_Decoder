import unittest
from libretranslator import escape_ansi, decode_data, translate_data

class TestDecoding(unittest.TestCase):
    def test_decode_data(self):
        self.assertEqual(decode_data("74656c6e6574"), "telnet", "Should be telnet")
        self.assertEqual(decode_data("1b5b313b33346dd0bfd0bed0bbd18cd0b7d0bed0b2d0b0d182d0b5d0bbd18c1b5b313b33336d3a201b5b306d"), "\x1b[1;34mпользователь\x1b[1;33m: \x1b[0m", "It should be an ansi escaped russian word.")
        self.assertEqual(decode_data("ce93ceb5ceb9ceac20cf83cebfcf85"), "Γειά σου", "It should be Greek saying hi.")
        self.assertEqual(decode_data("9df34588"), None, "Decoding should not be possible.")

class TestAnsiEscape(unittest.TestCase):
    def test_escape_ansi(self):
        self.assertEqual(escape_ansi("\x1b[1;34mпользователь\x1b[1;33m: \x1b[0m"), "пользователь: ", "Should be russian")
        self.assertEqual(escape_ansi("telnet"), "telnet", "ANSI escape should work with a clean string too.")

class TestTranslationService(unittest.TestCase):
    def test_translation(self):
        self.assertEqual(translate_data("こんにちは"), "Hello!", "Japanese to English translation.")
        self.assertEqual(translate_data("\x1b[1;34mпользователь\x1b[1;33m: \x1b[0m"), "User:", "Russian to English translation.")

if __name__ == '__main__':
    unittest.main()

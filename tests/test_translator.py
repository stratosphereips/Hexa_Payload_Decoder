import unittest
from libretranslator import escape_ansi, decode_data, translate_data

class TestDecoding(unittest.TestCase):
    def test_decode_data(self):
        self.assertEqual(decode_data("74656c6e6574"), "telnet", "Should be telnet")
        self.assertEqual(decode_data("1b5b313b33346dd0bfd0bed0bbd18cd0b7d0bed0b2d0b0d182d0b5d0bbd18c1b5b313b33336d3a201b5b306d"), "\x1b[1;34mпользователь\x1b[1;33m: \x1b[0m", "Should be russian")

class TestAnsiEscape(unittest.TestCase):
    def test_escape_ansi(self):
        self.assertEqual(escape_ansi("\x1b[1;34mпользователь\x1b[1;33m: \x1b[0m"), "пользователь: ", "Should be russian")
        self.assertEqual(escape_ansi("telnet"), "telnet", "Should work with clean string too")

if __name__ == '__main__':
    unittest.main()

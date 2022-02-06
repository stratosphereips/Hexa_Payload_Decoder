import sys
import re
from libretranslatepy import LibreTranslateAPI

# translator = LibreTranslateAPI('http://localhost:5000/')
translator = LibreTranslateAPI('https://translate.argosopentech.com/')

def escape_ansi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

data = sys.argv[1]
# print(data)

try:
    decoded_data = bytes.fromhex(data).decode('utf-8')
    escaped_data = escape_ansi(decoded_data)
    # print("Escaped data", escaped_data)

    languages = translator.detect(escaped_data)
    # print(languages)
    # for lang in languages:
    if languages[0]["confidence"] > 0.2:
        text = translator.translate(escaped_data, languages[0]["language"], 'en')
        print(text)
    else:
        for lang in ['en', 'ru', 'cn', 'es']:
            try:
                text = translator.translate(escaped_data, lang, 'en')
                print(text)
            except:
                pass 
except Exception as e: # UnicodeDecodeError may happen
    pass

import sys
import re
from libretranslatepy import LibreTranslateAPI

# translator = LibreTranslateAPI('http://localhost:5000/')
# translator = LibreTranslateAPI('https://translate.argosopentech.com/')
translator = LibreTranslateAPI('https://translate.mentality.rip/')

def escape_ansi2(line):
    # From https://superuser.com/a/1657976 and https://superuser.com/a/1388860
    re1 = re.compile(r'\x1b\[[\x30-\x3f]*[\x20-\x2f]*[\x40-\x7e]')
    re2 = re.compile(r'\x1b[PX^_].*?\x1b\\')
    re3 = re.compile(r'\x1b\][^\a]*(?:\a|\x1b\\)')
    re4 = re.compile(r'\x1b[\[\]A-Z\\^_@]')
    # re5: zero-width ASCII characters
    # see https://superuser.com/a/1388860
    re5 = re.compile(r'[\x00-\x1f\x7f-\x9f\xad]+')

    for r in [re1, re2, re3, re4, re5]:
        line = r.sub('', line)

    return line

def escape_ansi(line):
    # ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', line)

def decode_data(data):
    try:
        decoded_data = bytes.fromhex(data).decode('utf-8')
        return decoded_data
    except:
        return None 

def translate_data(data):
    try:
        escaped_data = escape_ansi(data)
        languages = translator.detect(escaped_data)
        # We are only looking at the first detected language
        if languages[0]["confidence"] > 0.2:
            text = translator.translate(escaped_data, languages[0]["language"], 'en')
            return text
        else:
            for lang in ['en', 'ru', 'cn', 'es']:
                try:
                    text = translator.translate(escaped_data, lang, 'en')
                    return text
                except:
                    return None 
    except Exception as e:
        return None


data = sys.argv[1]
# print(data)

try:
    decoded_data = bytes.fromhex(data).decode('utf-8')
    escaped_data = escape_ansi(decoded_data)

    languages = translator.detect(escaped_data)

    # We are only looking at the first detected language
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

import sys
import re
from googletrans import Translator

translator = Translator(service_urls=['translate.google.com'])

def escape_ansi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

data = sys.argv[1]
data = escape_ansi(data)
#print(sys.argv)
#print(data)

lang = translator.detect(data)
#print(lang)
text = translator.translate(data,dest='en', src=lang.lang)
print(text.text)

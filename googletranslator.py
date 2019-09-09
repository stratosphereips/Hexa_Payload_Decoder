import sys
from googletrans import Translator

translator = Translator()

data = sys.argv[1]
#print(sys.argv)
print(data)

t = translator.translate(data)
print(t.text)
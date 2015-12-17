from string import ascii_lowercase
import json


filename = 'keydict.py'
target = open(filename, 'w')

keydictionary = {}


for alpha in ascii_lowercase:
	keydictionary['key.' + alpha.upper()] = alpha

for letter in str(1234567890):
	keydictionary['key._' + letter] = letter

with open(filename, 'w') as f:
	json.dump(keydictionary, f)
import json

with open('macros.json') as f:
	for name, value in json.load(f).items():
		print(f'@define {name} {value.replace('\n', '\\n')}')
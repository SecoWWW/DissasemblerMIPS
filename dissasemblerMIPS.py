import json
from pprint import pprint


def openfile(file_name):
    with open(str(file_name)) as code:
        code = [code.rstrip('\n')]
    return code

def typeoffile(file):
    file[0]



with open('Mips-Instructions.json') as data:
    instructions = json.load(data)

pprint(instructions)

if __name__ == "__main__":
    print("Hlavna funkcia")
else:
    print("Importovana funkcia")




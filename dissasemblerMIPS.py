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

# pprint(instructions)

# print("{0:0{1}x}".format(40, 8)) # vypis adresy
# a mod b == a % b
# obycajny branch
# PC = i + 4
# C = (C << 2) % 65536
# C = (C if C<2**15 else C-2**16)
# PC = hex(PC+C)
PC = 104 + 4
C = (65519 << 2) % 65536
C = (C if C<2**15 else C-2**16)
print("{0:0{1}x}".format(PC+C, 8))
# # Type J instruction
# PC = i
# PC = (PC & 4026531840 | (A << 2))
# PC = (PC if PC<2**31 else PC-2**32)
PC = 54
PC =  (PC & 4026531840) | (67108863 << 2)
PC = (PC if PC<2**31 else PC-2**32)
print("{0:0{1}x}".format(PC, 8))
print(int("1101",2))
# i + 4 + (C << 2) % 65536 / 4 # 256**2 <-- pre vypocet adressy branch
if __name__ == "__main__":
    print("Hlavna funkcia")
else:
    print("Importovana funkcia")




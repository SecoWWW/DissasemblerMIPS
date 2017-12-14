import json
from pprint import pprint


def openfile(file_name):
    with open(str(file_name)) as code:
        code = [code.rstrip('\n')]
    return code

def typeoffile(file):
    file[0]





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
PC = 432
PC = (PC & int("0xf0000000", 16)) | (14745312 << 2)
PC = (PC if PC<2**31 else PC-2**32)
print("{0:0{1}x}".format(PC, 8))
print(int("1101",2))
# i + 4 + (C << 2) % 65536 / 4 # 256**2 <-- pre vypocet adressy branch
# with open('instructions.json') as data:
#     instructions = json.load(data)

    # print(instructions["instructions"][0]["R"])
    # for itterator in instructions["instructions"][0]["R"]:
    #     if itterator["s"] == True:
    #         print(itterator["s"])
# with open('instructions.json', "r") as data:
#     data.seek(12450)
#     chunk = data.read(100)
#     print(chunk)
with open("test.txt","w") as text:
    text.write("Prva veta.")
    text.write("druha veta.")
    text.seek(0)
    text.write("Treria veta.")

def biteOperations():
    with open("input.txt", "rb") as file:
        while True:
            chunk = file.read(1024)
            if chunk:
                for b in chunk:
                    print(bin(b)[2:])
                    for i in range(0,8):
                        byte = b & 128
                        print(bin(byte)[2:3],end='')
                        b = b << 1
                    print()

            else:
                break

if __name__ == "__main__":
    print("Hlavna funkcia")
else:
    print("Importovana funkcia")




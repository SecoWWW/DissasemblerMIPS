#with open("", "rb") as file:
import os
#import struct
os.chdir("examples/Ukazka1")
with open("ukazka1.o", "rb") as file:
    sum = 0
    chunk = file.read(52)
    for i in range(32,36):
        sum += int(chunk[i])*(256**(35-i))
print(sum)
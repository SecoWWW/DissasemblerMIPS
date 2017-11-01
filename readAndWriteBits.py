import binascii
import sys

def readElfHeader(file_location):
    with open(file_location, "rb") as file:
        section_offset = 0
        machine_version = 0
        section_size = 0
        number_of_sections = 0


        chunk = file.read(52)
        for i in range(18,20):                                  #start is at 18 and size is 2 bytes
            machine_version += int(chunk[i])*(256**(19-i))
        for i in range(32,36):                                  #start is at 32 and size is 4 bytes
            section_offset += int(chunk[i])*(256**(35-i))
        for i in range(46,48):                                  #start is at 46 and size is 2 bytes
            section_size += int(chunk[i])*(256**(47-i))
        for i in range(48,50):                                  #start is at 48 and size is 2 bytes
            number_of_sections += int(chunk[i])*(256**(49-i))

        file.seek(section_offset)
        text_index = []
        shstrtab_indexes = []
        for i in range(0,number_of_sections):
            print("Section address: " + str(hex(section_offset+(section_size*i))))
            chunk = file.read(section_size)
            sh_type = 0

            for j in range(4,8):
                sh_type += int(chunk[j])*(256**(7-j))
            print("Section type: " + str(sh_type))
            if(sh_type == 3):
                shstrtab_indexes.append(int(i))
                print("Found possible shstrtab section.")
            if(sh_type == 1):
                text_index.append(i)
                print("Found possible text section.")
            print()

        print(len(shstrtab_indexes))
        print("shstrtab_indexes is " + repr(shstrtab_indexes))
        print("text_index is " + repr(text_index))

        if shstrtab_indexes is None:
            sys.stderr.write("shstrtab_indexes is type None\n")
            return

        shstrtab_offset = findShstrtab(section_offset, section_size, shstrtab_indexes)
        print(shstrtab_offset)
        file.seek(shstrtab_offset+1)
        # shstrtab_size = 100
        # string = ""
        # for i in range(0,shstrtab_size):
        #     chunk = file.read(1)
        #     string += chr(int(chunk[0]))
        # print(string)



    print("Machine version: " + str(machine_version))
    print("Section offset (from start of file): " + str(section_offset))
    print("Each section header size: " + str(section_size))
    print("Number of sections: " + str(number_of_sections))




def findShstrtab(section_offset, section_size, indexes):
    if(len(indexes) <= 0):
        sys.stderr.write("In findShstrtab() empty list was send\n")
        return 0

    with open(file_location, "rb") as file:
        for i in indexes:
            file.seek(section_offset+(i*section_size))
            chunk = file.read(section_size)

            sh_name = 0
            sh_size = 0
            sh_offset = 0

            for j in range(0, 4):
                sh_name += int(chunk[j]) * (256 ** (3 - j))
            for j in range(16, 20):
                sh_offset += int(chunk[j]) * (256 ** (19 - j))
            for j in range(20, 24):
                sh_size += int(chunk[j]) * (256 ** (23 - j))

            file.seek(sh_offset+sh_name)
            name = file.read(len(".shstrtab"))
            print(name.decode("utf-8"))
            if(name.decode("utf-8") == ".shstrtab"):
                print(sh_offset)
                return sh_offset





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

file_location = "examples/Ukazka2/ukazka2.o"
readElfHeader(file_location)
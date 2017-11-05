import sys


def readElfHeader():
    with open(file_location, "rb") as file:
        section_offset = 0
        machine_version = 0
        section_size = 0
        number_of_sections = 0

        chunk = file.read(52)
        for i in range(18, 20):
            # start is at 18 and size is 2 bytes
            machine_version += int(chunk[i])*(256**(19-i))
        for i in range(32, 36):
            # start is at 32 and size is 4 bytes
            section_offset += int(chunk[i])*(256**(35-i))
        for i in range(46, 48):
            # start is at 46 and size is 2 bytes
            section_size += int(chunk[i])*(256**(47-i))
        for i in range(48, 50):
            # start is at 48 and size is 2 bytes
            number_of_sections += int(chunk[i])*(256**(49-i))

        file.seek(section_offset)
        text_indexes = []
        shstrtab_indexes = []
        for i in range(0, number_of_sections):
            # print("Section address: " + str(hex(section_offset+(section_size*i))))
            chunk = file.read(section_size)
            sh_type = 0

            for j in range(4, 8):
                sh_type += int(chunk[j])*(256**(7-j))
            # print("Section type: " + str(sh_type))
            if sh_type == 3:
                shstrtab_indexes.append(int(i))
                # print("Found possible shstrtab section.")
            if sh_type == 1:
                text_indexes.append(i)
                # print("Found possible text section.")
            # print()

        print(len(shstrtab_indexes))
        print("shstrtab_indexes is " + repr(shstrtab_indexes))
        print("text_index is " + repr(text_indexes))

        if shstrtab_indexes is None:
            sys.stderr.write("shstrtab_indexes is type None\n")
            return

        shstrtab_offset = findShstrtab(section_offset,
                                       section_size,
                                       shstrtab_indexes)
        # print(shstrtab_offset)
        # file.seek(shstrtab_offset+1)
        # shstrtab_size = 100
        # string = ""
        # for i in range(0,shstrtab_size):
        #     chunk = file.read(1)
        #     string += chr(int(chunk[0]))
        # print(string)
        text_offset, text_size = findText(section_offset,
                                          section_size,
                                          text_indexes,
                                          shstrtab_offset)
        # print("text_offset is: " + str(text_offset))
        # print("text_size is: " + str(text_size))

        # file.seek(text_offset)
        # for i in range(0,text_size,4):
        #     chunk = file.read(4)
        #     for j in range(0,4):
        #         print(format(int(chunk[j]), "x"),end="")
        #     print()

        dissasemble(text_offset,text_size)


    # print("Machine version: " + str(machine_version))
    # print("Section offset (from start of file): " + str(section_offset))
    # print("Each section header size: " + str(section_size))
    # print("Number of sections: " + str(number_of_sections))


def findShstrtab(section_offset, section_size, indexes):
    if len(indexes) <= 0:
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
            # print(name.decode("utf-8"))
            if name.decode("utf-8") == ".shstrtab":
                # print(sh_offset)
                return sh_offset


def findText(section_offset, section_size, text_indexes, shstrtab_offset):
    with open(file_location, "rb") as file:
        for i in text_indexes:
            file.seek(section_offset+(section_size*i))
            chunk = file.read(section_size)

            sh_name = 0
            for j in range(0, 4):
                sh_name += int(chunk[j]) * (256 ** (3 - j))

            file.seek(shstrtab_offset + sh_name)
            name = file.read(len(".text"))
            print(name.decode("utf-8"))
            text_offset = 0
            text_size = 0
            if name.decode("utf-8") == ".text":
                for j in range(16, 20):
                    text_offset += int(chunk[j]) * (256 ** (19 - j))
                for j in range(20, 24):
                    text_size += int(chunk[j]) * (256 ** (23 - j))
                return text_offset, text_size

def dissasemble(offset, size):
    with open(file_location, "rb") as file:
        file.seek(offset)
        for i in range(0,size,4):
            instruction = file.read(4)

            opcode = ""
            funct = ""
            regimm = ""
            reg_s = ""
            reg_t = ""
            reg_d = ""
            imm_S = ""
            imm_C = ""
            add_A = ""
            # for b in instruction:
            #     print("Whole byte: "+ str(bin(b)[2:]))
            #     for j in range(0, 6):
            #         byte = b & 128
            #         # print(bin(byte)[2:3], end='')
            #         opcode += str(bin(byte)[2:3])
            #         b = b << 1
            #     print(opcode)
            print("Whole byte 0: " + str(hex(instruction[0])))# 31 - 24
            print("Whole byte 1: " + str(hex(instruction[1])))# 23 - 16
            print("Whole byte 2: " + str(hex(instruction[2])))# 15 - 8
            print("Whole byte 3: " + str(hex(instruction[3])))# 7 - 0
            byte = instruction[0]
            for i in range(0,6):
                # 6 bits of 31 = 26 bits
                b = byte & 128
                opcode += str(bin(b)[2:3])
                byte = byte << 1

            if opcode == "000000":
                print("R type instruction")

                for i in range(0,2):
                    # 2 bits of 26 = 24 bits
                    b = byte % 128
                    reg_s += str(bin(b)[2:3])
                    byte = byte << 1
                byte = instruction[1]
                # next byte
                for i in range(0,3):
                    # 3 bits of 24 bits = 21 bits
                    b = byte & 128
                    reg_s += str(bin(b)[2:3])
                    byte = byte << 1
                for i in range(0,5):
                    # 5 bits of 21 = 16 bits
                    b = byte & 128
                    reg_t += str(bin(b)[2:3])
                    byte = byte << 1
                byte = instruction[2]
                for i in range (0,5):
                    # 5 bits of 16 = 11 bits
                    b = byte & 128
                    reg_t += str(bin(b)[2:3])
                    byte = byte << 1

            elif opcode == "000001":
                print("RI type instruction")
            elif opcode == "000001":
                print("J type instruction")
            else:
                print("I type instruction")


def registerName(number):
    if number == 0:
        return "$zero"
    elif number == 1:
        return "$at"
    elif number == 2:
        return "$v0"
    elif number == 3:
        return "$v1"
    elif number == 4:
        return "$a0"
    elif number == 5:
        return "$a1"
    elif number == 6:
        return "$a2"
    elif number == 7:
        return "$a3"
    elif number == 8:
        return "$t0"
    elif number == 9:
        return "$t1"
    elif number == 10:
        return "$t2"
    elif number == 11:
        return "$t3"
    elif number == 12:
        return "$t4"
    elif number == 13:
        return "$t5"
    elif number == 14:
        return "$t6"
    elif number == 15:
        return "$t7"
    elif number == 16:
        return "$s0"
    elif number == 17:
        return "$s1"
    elif number == 18:
        return "$s2"
    elif number == 19:
        return "$s3"
    elif number == 20:
        return "$s4"
    elif number == 21:
        return "$s5"
    elif number == 22:
        return "$s6"
    elif number == 23:
        return "$s7"
    elif number == 24:
        return "$t8"
    elif number == 25:
        return "$t9"
    elif number == 26:
        return "$k0"
    elif number == 27:
        return "$k1"
    elif number == 28:
        return "$gp"
    elif number == 29:
        return "$sp"
    elif number == 30:
        return "$fp"
    else:
        return "$ra"

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

file_location = "examples/Ukazka1/ukazka1.o"
readElfHeader()
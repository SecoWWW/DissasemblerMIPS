#!/usr/bin/env python3
import sys
import json
import getopt

file_location = "examples/Ukazka1/ukazka1.o"
output_location = "examples/Ukazka1/dissassembled2.txt"
program_name = 'dissassembler.py'
i_option = False
o_option = False
x_option = False

def readElfHeader():
    with open(file_location, "rb") as file:
        print(file_location)
        section_offset = 0
        machine_version = 0
        section_size = 0
        number_of_sections = 0

        chunk = file.read(52)
        for i in range(18, 20):
            # start is at 18 and size is 2 bytes
            machine_version += int(chunk[i])*(256**(19-i))
        # print(machine_version)
        if machine_version != 8:
            print("Error: Unkown architekture")
            return
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

        #
        # print(len(shstrtab_indexes))
        # print("shstrtab_indexes is " + repr(shstrtab_indexes))
        # print("text_index is " + repr(text_indexes))

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
            # print(name.decode("utf-8"))
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
        dissassembled_code = []
        dissassembled_code.append("address  bytes       decoded instructions")
        dissassembled_code.append("-----------------------------------------")
        address_label = []
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
            # print("Whole byte 0: " + str(hex(instruction[0])) + " " + bin(instruction[0]))# 31 - 24
            # print("Whole byte 1: " + str(hex(instruction[1])) + " " + bin(instruction[1]))# 23 - 16
            # print("Whole byte 2: " + str(hex(instruction[2])) + " " + bin(instruction[2]))# 15 - 8
            # print("Whole byte 3: " + str(hex(instruction[3])) + " " + bin(instruction[3]))# 7 - 0

            byte = instruction[0]               # first bit
            for j in range(0,6):
                # 6 bits of 32 = 26 bits
                b = byte & 128
                opcode += str(bin(b)[2:3])
                byte = byte << 1

            if opcode == "000000":
                # print("R type instruction")
                for j in range(0,2):
                    # 2 bits of 26 = 24 bits
                    b = byte & 128
                    reg_s += str(bin(b)[2:3])
                    byte = byte << 1
                byte = instruction[1]           # second bit
                for j in range(0,3):
                    # 3 bits of 24 bits = 21 bits
                    b = byte & 128
                    reg_s += str(bin(b)[2:3])
                    byte = byte << 1
                for j in range(0,5):
                    # 5 bits of 21 = 16 bits
                    b = byte & 128
                    reg_t += str(bin(b)[2:3])
                    byte = byte << 1
                byte = instruction[2]           # third bit
                for j in range(0,5):
                    # 5 bits of 16 = 11 bits
                    b = byte & 128
                    reg_d += str(bin(b)[2:3])
                    byte = byte << 1
                for j in range(0,3):
                    # 3 bits of 11 bits = 8 bits
                    b = byte & 128
                    imm_S += str(bin(b)[2:3])
                    byte = byte << 1
                byte = instruction[3]           # fourth bit
                for j in range(0,2):
                    # 2 bits of 8 = 6 bits
                    b = byte & 128
                    imm_S += str(bin(b)[2:3])
                    byte = byte << 1
                for j in range(0,6):
                    # 6 bits of 6 = 0 bits
                    b = byte & 128
                    funct += str(bin(b)[2:3])
                    byte = byte << 1
                # print(" opcode: "+ str(int(opcode, 2)) +" reg_s: "+ str(int(reg_s, 2)) +" reg_t: "+str(int(reg_t, 2))
                #       +" reg_d: "+str(int(reg_d, 2)) +" imm_S: "+str(int(imm_S, 2)) +" funct: "+str(int(funct, 2)))

                reg_s = registerName(int(reg_s, 2))
                reg_t = registerName(int(reg_t, 2))
                reg_d = registerName(int(reg_d, 2))
                imm_S = int(imm_S, 2)
                funct = int(funct, 2)

                # print(" opcode: " + str(int(opcode, 2)) + " reg_s: " + str(reg_s) + " reg_t: " + str(reg_t)
                #       + " reg_d: " + str(reg_d) + " imm_S " + str(imm_S) + " funct: " + str(funct))
                with open("instructions.json", "r") as json_file:
                    instructions = json.load(json_file)
                    if reg_s == "$zero" and reg_t == "$zero" and reg_d == "$zero" and imm_S == 0 and funct == 0:
                        syntax = "{0:0{1}x}".format(i, 8)
                        syntax += " " + "{0:0{1}x}".format(int(instruction[0]), 2) + "{0:0{1}x}".format(
                            int(instruction[1]), 2) + "{0:0{1}x}".format(int(instruction[2]), 2) \
                                  + "{0:0{1}x}".format(int(instruction[3]), 2)
                        syntax += "    nop"
                        dissassembled_code.append(syntax)
                        continue
                    for itterator in instructions["instructions"][0]["R"]:
                        if itterator["funct"] == funct:
                            syntax = "{0:0{1}x}".format(i, 8)
                            syntax += " " + "{0:0{1}x}".format(int(instruction[0]), 2) + "{0:0{1}x}".format(
                                int(instruction[1]), 2) + "{0:0{1}x}".format(int(instruction[2]), 2) \
                                      + "{0:0{1}x}".format(int(instruction[3]), 2)
                            syntax += "    " + itterator["syntax"]
                            if itterator["s"] == True:
                                syntax = syntax.replace("$s", reg_s)
                            if itterator["t"] == True:
                                syntax = syntax.replace("$t", reg_t)
                            if itterator["d"] == True:
                                syntax = syntax.replace("$d", reg_d)
                            if itterator["S"] == True:
                                syntax = syntax.replace("S", str(imm_S))
                            dissassembled_code.append(syntax)
                            break



            elif opcode == "000001":
                # print("RI type instruction")

                for j in range(0,2):            # first byte
                    # 2 bits of 26 = 24 bits
                    b = byte & 128
                    reg_s += str(bin(b)[2:3])
                    byte = byte << 1
                byte = instruction[1]           # second byte
                for j in range(0,3):
                    # 3 bits of 24 bits = 21 bits
                    b = byte & 128
                    reg_s += str(bin(b)[2:3])
                    byte = byte << 1
                for j in range(0,5):
                    # 5 bits of 21 = 16 bits
                    b = byte & 128
                    regimm += str(bin(b)[2:3])
                    byte = byte << 1
                byte = instruction[2]           # third byte
                for j in range(0,8):
                    # 8 bits of 16 = 8 bits
                    b = byte & 128
                    imm_C += str(bin(b)[2:3])
                    byte = byte << 1
                byte = instruction[3]           # fourth byte
                for j in range(0,8):
                    # 8 bits of 8 bits = 0 bits
                    b = byte & 128
                    imm_C += str(bin(b)[2:3])
                    byte = byte << 1
                imm_C = int(imm_C, 2)
                imm_C = (imm_C if imm_C < 2**15 else imm_C - 2**16)
                # print("opcode: "+ str(int(opcode, 2)) +" reg_s: "+ str(int(reg_s, 2)) +" regimm: "+str(int(regimm, 2))
                #       +" imm_C "+str(imm_C))

                reg_s = registerName(int(reg_s, 2))
                regimm = int(regimm, 2)

                # print("opcode: " + str(int(opcode, 2)) + " reg_s: " + str(reg_s) + " regimm: " + str(regimm)
                #       + " imm_C " + str(imm_C))
                with open("instructions.json", "r") as json_file:
                    instructions = json.load(json_file)
                    for itterator in instructions["instructions"][1]["RI"]:
                        if itterator["regimm"] == regimm:
                            syntax = "{0:0{1}x}".format(i, 8)
                            syntax += " " + "{0:0{1}x}".format(int(instruction[0]), 2) + "{0:0{1}x}".format(
                                int(instruction[1]), 2) + "{0:0{1}x}".format(int(instruction[2]), 2) \
                                      + "{0:0{1}x}".format(int(instruction[3]), 2)
                            syntax += "    " + itterator["syntax"]
                            if itterator["s"] == True:
                                syntax = syntax.replace("$s", reg_s)
                            if itterator["C"] == True:
                                if syntax[21] == 'b':
                                    # syntax += "it is branch instruction"
                                    PC = i + 4
                                    imm_C = (imm_C << 2) % 65536
                                    imm_C = (imm_C if imm_C < 2**15 else imm_C-2**16)
                                    address = "{0:0{1}x}".format(PC + imm_C, 8)
                                    imm_C = "loc_" + address
                                    address_label.append(address + "     " + imm_C + ":")

                                syntax = syntax.replace("C", str(imm_C))

                            dissassembled_code.append(syntax)
                            break

            elif (opcode == "000010" or opcode == "000011"):
                # print("J type instruction")

                for j in range(0, 2):            # first byte
                    # 2 bits of 26 = 24 bits
                    b = byte & 128
                    add_A += str(bin(b)[2:3])
                    byte = byte << 1
                byte = instruction[1]           # second byte
                for j in range(0, 8):
                    # 8 bits of 24 = 16 bits
                    b = byte & 128
                    add_A += str(bin(b)[2:3])
                    byte = byte << 1
                byte = instruction[2]           # third byte
                for j in range(0, 8):
                    # 8 bits of 16 = 8 bits
                    b = byte & 128
                    add_A += str(bin(b)[2:3])
                    byte = byte << 1
                byte = instruction[3]           # fourth byte
                for j in range(0, 8):
                    # 8 bits of 8 = 0 bits
                    b = byte & 128
                    add_A += str(bin(b)[2:3])
                    byte = byte << 1

                opcode = int(opcode, 2)
                add_A = int(add_A, 2)
                PC = i
                PC = (PC & int("0xf0000000", 16)) | (add_A << 2)
                add_A = (PC if PC < 2 ** 31 else PC - 2 ** 32)

                # print("opcode: " + str(opcode) + " add_A: " + str(add_A))

                with open("instructions.json", "r") as json_file:
                    instructions = json.load(json_file)
                    for itterator in instructions["instructions"][2]["J"]:
                        if itterator["opcode"] == opcode:
                            syntax = "{0:0{1}x}".format(i, 8)
                            syntax += " " + "{0:0{1}x}".format(int(instruction[0]), 2) + "{0:0{1}x}".format(
                                int(instruction[1]), 2) + "{0:0{1}x}".format(int(instruction[2]), 2) \
                                      + "{0:0{1}x}".format(int(instruction[3]), 2)
                            syntax += "    " + itterator["syntax"]
                            address = "{0:0{1}x}".format(add_A, 8)
                            address_label.append(address + "     " + "loc_" + address + ":")
                            # for j in range(0, len(dissassembled_code)):
                            #     if str.rfind(dissassembled_code[j], address, 0, 8) != -1:
                            #         dissassembled_code.insert(j, address + "     " + add_A)
                            #         break
                            syntax = syntax.replace("A", "loc_"+address)
                            dissassembled_code.append(syntax)
                            break


            else:
                # print("I type instruction")
                for j in range(0,2):            # first byte
                    # 2 bits of 26 = 24 bits
                    b = byte & 128
                    reg_s += str(bin(b)[2:3])
                    byte = byte << 1
                byte = instruction[1]           # second byte
                for j in range(0,3):
                    # 3 bits of 24 bits = 21 bits
                    b = byte & 128
                    reg_s += str(bin(b)[2:3])
                    byte = byte << 1
                for j in range(0,5):
                    # 5 bits of 21 = 16 bits
                    b = byte & 128
                    reg_t += str(bin(b)[2:3])
                    byte = byte << 1
                byte = instruction[2]           # third byte
                for j in range(0,8):
                    # 8 bits of 16 = 8 bits
                    b = byte & 128
                    imm_C += str(bin(b)[2:3])
                    byte = byte << 1
                byte = instruction[3]           # fourth byte
                for j in range(0,8):
                    # 8 bits of 8 bits = 0 bits
                    b = byte & 128
                    imm_C += str(bin(b)[2:3])
                    byte = byte << 1
                imm_C = int(imm_C, 2)
                imm_C = (imm_C if imm_C<2**15 else imm_C-2**16)

                # print("opcode: "+str(int(opcode, 2)) + " reg_s: " + str(int(reg_s, 2)) + " reg_t: " + str(int(reg_t, 2))
                #       + " imm_C: "+ str(imm_C))

                opcode = int(opcode, 2)
                reg_s = registerName(int(reg_s, 2))
                reg_t = registerName(int(reg_t, 2))

                # print("opcode: " + str(opcode) + " reg_s: " + str(reg_s) + " reg_t: " + str(reg_t)
                #       + " imm_C: " + str(imm_C))

                with open("instructions.json", "r") as json_file:
                    instructions = json.load(json_file)
                    for itterator in instructions["instructions"][3]["I"]:
                        if itterator["opcode"] == opcode:
                            syntax = "{0:0{1}x}".format(i, 8)
                            syntax += " " + "{0:0{1}x}".format(int(instruction[0]), 2) + "{0:0{1}x}".format(
                                int(instruction[1]), 2) + "{0:0{1}x}".format(int(instruction[2]), 2) \
                                      + "{0:0{1}x}".format(int(instruction[3]), 2)
                            syntax += "    " + itterator["syntax"]
                            if itterator["s"] == True:
                                syntax = syntax.replace("$s", reg_s)
                            if itterator["t"] == True:
                                syntax = syntax.replace("$t", reg_t)
                            if itterator["C"] == True:
                                if syntax[21] == 'b':
                                    # syntax += "it is branch instruction"
                                    PC = i + 4
                                    imm_C = (imm_C << 2) % 65536
                                    imm_C = (imm_C if imm_C < 2**15 else imm_C-2**16)
                                    address = "{0:0{1}x}".format(PC + imm_C, 8)
                                    imm_C = "loc_" + address
                                    address_label.append(address + "     " + imm_C + ":")


                                syntax = syntax.replace("C", str(imm_C))
                            dissassembled_code.append(syntax)
                            break
    for i in range(0,len(dissassembled_code)):
        for j in range(0,len(address_label)):
            if str.rfind(dissassembled_code[i], address_label[j][0:8], 0, 8) != -1:
                if dissassembled_code[i-1] == address_label[j]:
                    # print("the same are here")
                    del address_label[j]
                    break
                dissassembled_code.insert(i, address_label[j])
                # print(dissassembled_code[i] + " " + address_label[j])
                del address_label[j]
                break
    if (o_option == True):
        with open(output_location, "w") as file:
            for output_line in dissassembled_code:
                if x_option == True:
                    file.write(output_line + "\n")
                else:
                    if output_line[13:16] == "loc":
                        file.write(output_line[13:] + "\n")
                        continue
                    file.write(output_line[19:] + "\n")
    else:
        for output_line in dissassembled_code:
            if x_option == True:
                print(output_line)
            else:
                if output_line[13:16] == "loc":
                    print(output_line[13:])
                    continue
                print(output_line[19:])





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






def printhelp(name):
    print("usage: " + name + "     [-h] | [-x] | [-o] -i <input file>")
    print("\nProcess .elf file for MIPS 32-bit architecture ")
    print("\n Required:====================================")
    print("  -i     specify path to input file")
    print("\n Optional:====================================")
    print("  -o     specify path to output file")
    print("  -x     print also address of instruction and \n"
          "         hex format of instruction")
    print("  -h     help")
    sys.exit(1)

if __name__ == "__main__":
    # main(sys.argv)
    if len(sys.argv) == 1:
        printhelp(sys.argv[0])
    for arg in range(0, len(sys.argv)):
        if sys.argv[arg] == "-h":
            printhelp(sys.argv[0])
        elif sys.argv[arg] == "-i":
            # print("input file: " + sys.argv[arg+1])
            if len(sys.argv) <= arg + 1:
                print("  No input file")
                sys.exit(1)
            file_location = sys.argv[arg+1]
            i_option = True
        elif sys.argv[arg] == "-o":
            # print("output file: " + sys.argv[arg + 1])
            if len(sys.argv) <= arg + 1:
                print("  No output file")
                sys.exit(1)
            output_location = sys.argv[arg + 1]
            o_option = True
        elif sys.argv[arg] == "-x":
            x_option = True
    if(i_option == False):
        print("No input file")
        sys.exit(1)

    readElfHeader()
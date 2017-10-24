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

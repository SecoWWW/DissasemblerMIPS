s = "00000000     bltz $s, C\n00000004     bgez $s, C\n"
d = "00000004 loc_00000004\n"
s = s[:24] + d + s[24:]
print(s)
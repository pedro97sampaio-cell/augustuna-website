import sys

with open("index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if i == 815:
        skip = True
        new_lines.append(open("festivais.html", "r", encoding="utf-8").read() + "\n")
    if i == 889:
        skip = False
        continue
    
    if i == 908:
        skip = True
        new_lines.append(open("outras.html", "r", encoding="utf-8").read() + "\n")
    if i == 987:
        skip = False
        continue
        
    if i == 990:
        skip = True
    if i == 1068:
        skip = False
        continue
    
    if not skip:
        new_lines.append(line)

with open("index.html", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
print("Updated index.html successfully.")

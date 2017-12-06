import os

for filename in os.listdir("../Output"):
    f = open("../Output/" + filename, "r")
    for line in f.readlines()[1:]:
        qval = float(line.split(" ")[2])
        if qval == 0:
            print line

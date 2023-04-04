import random
def off_cv():
    off_cv = []
    with open(file="./bin/source/off.cv", mode="r", encoding="utf-8") as file:
        for i in file.readlines():
            off_cv.append(i.strip())
        return str(random.choice(off_cv))
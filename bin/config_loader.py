import time
from bin import ctc
#===============
def load_playchannel() :
    file_ = "play_channel.cfg"
    playchannel = []
    with open(file = f"./config/{file_}", mode = "r", encoding = "utf-8") as id_ :
        end = False
        while end == False :
            id = id_.readline().strip("\n")
            if id == ".end" :
                end = True
            else :
                playchannel.append(int(id))

    ctc.printBlue(f"{file_} loaded...\n")
    print("channel_id:")
    for w in playchannel :
        ctc.printDarkGreen(str(w)+"\n")
    time.sleep(0.5)
    return playchannel

    #===============

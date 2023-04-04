from bin import ctc
import sys
def token(token):
    if token == None :
        try :
            with open(file="./config/client.token", mode="r", encoding="utf-8") as file:
                token = file.readline()
                return token
        except Exception:
            ctc.printRed("can't load client.token")
            sys.exit(-1)
    else :
        return token

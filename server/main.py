#!/usr/bin/env python3

from server import newRPCServer
from stub import *

def main():
    
    # server is instantiated
    serv = newRPCServer(port=8080)
    
    # functions are then registerd with the RPCHandler class. Note this is delegated
    serv.register_function(add)
    serv.register_function(ping)
    
    # server is then set to listen
    serv.run()

if __name__ == "__main__":
    main()

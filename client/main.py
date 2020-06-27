#!/usr/bin/env python3

from client import newRPCProxy

def main():
    proxy = newRPCProxy(ip='127.0.0.1', port=8080)

    # all functions registered with the RPCHandler class can then be called

    ret = proxy.ping()
    print(ret)

    a = proxy.add(2,5)
    print(a)

    res = proxy.ha()
    print(res)

if __name__ == "__main__":
    main()

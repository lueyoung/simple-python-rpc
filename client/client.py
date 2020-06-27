from socket import *
import pickle

class RPCProxy():
    """Proxy class for a socket, which delegates the RPC using the RPCHandler class


    Parameters
    ----------
    connection: socket object
        socket object to be wrapped

    """

    def __init__(self, connection):

        self._connection = connection

    def __getattr__(self, name):

        def do_rpc(*args, **kwargs):

            try:

                # the socket sends the name of the attribute, along with the arguments to the server (which in turn passes the socket down to the RPCHandler class) in the form of a pickled tuple

                self._connection.send(pickle.dumps((name, args, kwargs)))

                # the result is then returned by the RPCHandler

                result = pickle.loads(self._connection.recv(1028))

                if isinstance(result, Exception):
                    raise Exception

            except Exception as err:
                print(err)

            return result
        return do_rpc

def newRPCProxy(ip="0.0.0.0", port=8080):
    # a socket is instantiated and connected to the server
    sock = socket(AF_INET, SOCK_STREAM)
    serv_addr = (ip, port)
    sock.connect(serv_addr)

    # once the socket is connected, it is wrapped with the Proxy class

    proxy = RPCProxy(sock)
    return proxy

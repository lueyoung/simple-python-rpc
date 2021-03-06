import pickle
from socket import *
from threading import Thread

class RPCHandler():
    """Class thant handles RPC; must be ussed in conjuction with some form of server"""

    def __init__(self):

        # functions are registered and stored in a dictionary with the function name as keys

        self._functions = {}

    def register_function(self, func):
        """Method used to register function

        Parameters
        ----------
        func: function object
            function to be stored

        """
        self._functions[func.__name__] = func

    def handle_connection(self, connection):
        """Method that handles RPC

        Parameters
        ----------
        connection: socket object
            socket object connected to the server containing the RPCHandler class. Note that the best way to implement this class is to generate a proxy wrapper class for a socket

        """

        try:
            while True:

                # the function name and arguments are sent in the form of a serialized tuple

                func_name, args, kwargs = pickle.loads(connection.recv(1028))

                if func_name not in self._functions:
                    res = "{} is not registerd".format(func_name)
                    connection.send(pickle.dumps(res))
                    print(res)
                    continue

                try:

                    # the function is then called with the arguments

                    result = self._functions[func_name](*args, **kwargs)

                    # and the result is pickled and sent back to the connecting socket

                    connection.send(pickle.dumps(result))

                except Exception as err:
                    print(err)
                    continue

        except EOFError:
            pass


class RPCServer(socket):

    port = 8080

    """TCP server that implements the RPCHandler class to handle remote procedure calls"""

    def __init__(self):

        super().__init__(AF_INET, SOCK_STREAM)

        self.handler = RPCHandler()


    def serve_forever(self):
        """Method called to start the server"""

        IP = gethostbyname(gethostname())
        PORT = self.port

        self.bind((IP, PORT))
        self.listen()

        while True:

            print('Waiting for Connection at IP: {} PORT: {}'.format(IP, PORT))

            client_sock, client_addr = self.accept()

            print('Connecion made at {}'.format(client_addr))

            # once a connection has been made, the socket (which is ideally wrapped with a proxy class) is passed down to the handler

            t = Thread(target=self.handle_connection, args=(client_sock,))
            t.start()
        
        self.close()


    def __getattr__(self, name):
        return getattr(self.handler, name)

    def config(self, port):
        self.port = port

    def run(self):
        self.serve_forever()

def newRPCServer(port=8080):
    serv = RPCServer()
    serv.config(port)
    return serv

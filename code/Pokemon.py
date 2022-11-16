import pokemon_ou_pb2
import pokemon_ou_pb2_grpc
import grpc
import time

class Pokemon:
    name = ""
    path = []

    def Path(self):
        return self.path

    def __init__(self):
        with grpc.insecure_channel('server:50051') as channel:  
            stub = pokemon_ou_pb2_grpc.gameserverStub(channel)
            time.sleep(1)
            res = stub.Connect(pokemon_ou_pb2.ConnectMessage(type = 'poke'))
            self.name = res.status
            self.path.append(res.pos)
            print("Pokemon: " + self.name + " is at ", self.path[0])
            stub.Board(pokemon_ou_pb2.Empty())
            caught = 0
            while(caught!=1):
               break

import pokemon_ou_pb2
import pokemon_ou_pb2_grpc
import grpc
import time


class Trainer:
    name = ""
    path = []
    pokedex = []

    def Path(self):
        return self.path

    def Pokedex(self):
        return self.pokedex

    def __init__(self):
        with grpc.insecure_channel('server:50051') as channel:  
            stub = pokemon_ou_pb2_grpc.gameserverStub(channel)
            time.sleep(1.5)
            res = stub.Connect(pokemon_ou_pb2.ConnectMessage(type = 'train'))
            self.name = res.status
            self.path.append(res.pos)
            #print("Trainer: " + self.name + " is at ", self.path[0])
           # stub.Board(pokemon_ou_pb2.Empty())
            gameOver = 0
            while gameOver ==0:
                dog = 2
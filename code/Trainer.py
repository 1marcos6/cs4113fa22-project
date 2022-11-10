import pokemon_ou_pb2
import pokemon_ou_pb2_grpc
import grpc


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
            name = stub.Connect(pokemon_ou_pb2.ConnectMessage(type = 'train')).type
            self.name = name
            gameOver = 0
            while gameOver ==0:
                break
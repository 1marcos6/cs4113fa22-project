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
            name = stub.Connect(pokemon_ou_pb2.ConnectMessage(type = 'poke')).type
            self.name = name
            caught = 0
            while(caught!=1):
                time.sleep(0.5)

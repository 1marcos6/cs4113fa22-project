import pokemon_ou_pb2
import pokemon_ou_pb2_grpc
import grpc
import time
import random

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
            res = stub.Connect(pokemon_ou_pb2.ConnectMessage(type = 'train'))
            self.name = res.status
            self.path.append(res.pos)
            gameOver = 0
            time.sleep(10)
            while gameOver ==0:
                res = stub.BoardCheck(pokemon_ou_pb2.CurrentLocation(type = 'train', location = self.path[-1]))
                if(len(res.moves) > 0):
                     #print(res.moves)
                     move = int(res.moves[0])
                     moveResponse = stub.MoveRequest(pokemon_ou_pb2.MoveRequestMessage(type = 'train', name = self.name, move = move, curr = self.path[-1]))
                     if moveResponse.status != 'no':
                        self.path.append(move)
                     if moveResponse.status == 'poke':
                        ##try to catch
                        res = stub.Capture(pokemon_ou_pb2.CaptureReq(pos = self.path[-1]))
                        if(len(res.names) > 0):
                            #rint("I caught all of these: " + str(res.names))
                            for pokemon in res.names:
                                self.pokedex.append(pokemon)
                    
                time.sleep(1.1)

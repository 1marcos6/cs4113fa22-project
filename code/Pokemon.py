import pokemon_ou_pb2
import pokemon_ou_pb2_grpc
import grpc
import time
import random

class Pokemon:
    name = ""
    path = []

    def Path(self):
        return self.path

    def __init__(self):
        with grpc.insecure_channel('server:50051') as channel:  
            stub = pokemon_ou_pb2_grpc.gameserverStub(channel)
            res = stub.Connect(pokemon_ou_pb2.ConnectMessage(type = 'poke'))
            self.name = res.status
            self.path.append(res.pos)

            caught = 0
            time.sleep(10)
            while(caught!=1):
               #check board
                res = stub.BoardCheck(pokemon_ou_pb2.CurrentLocation(type = 'poke', location = self.path[-1]))
                #print(res.moves)
                if(len(res.moves) > 0):
                    #get random element from moves array
                    move = int(res.moves[random.randint(0,len(res.moves)-1)])
                    #move to that location
                    moveResponse = stub.MoveRequest(pokemon_ou_pb2.MoveRequestMessage(type = 'poke', name = self.name, move = move, curr = self.path[-1]))
                    if moveResponse.status == 'yes':
                        self.path.append(move)
                time.sleep(2)

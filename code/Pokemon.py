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
                if (len(res.starmoves) > 0):
                    move = int(res.starmoves[random.randint(0,len(res.starmoves)-1)])
                elif(len(res.moves) > 0):
                    move = int(res.moves[random.randint(0,len(res.moves)-1)])
        
                moveResponse = stub.MoveRequest(pokemon_ou_pb2.MoveRequestMessage(type = 'poke', name = self.name, move = move, curr = self.path[-1]))
                   
                if moveResponse.status != 'no':
                        self.path.append(move)
                if moveResponse.status == 'Captured':
                        caught = 1



            res = stub.isGameOver(pokemon_ou_pb2.Empty())
            while(res.status == 'no'):
                time.sleep(2)
                res = stub.isGameOver(pokemon_ou_pb2.Empty())
            #silent disconnect from server


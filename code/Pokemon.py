import pokemon_ou_pb2
import pokemon_ou_pb2_grpc
import grpc
import time
import random

class Pokemon:
    name = "" # name of pokemon
    path = [] # path of pokemon

    def Path(self): # return path of pokemon
        return self.path

    def __init__(self): # constructor
        with grpc.insecure_channel('server:50051') as channel: # connect to server
            stub = pokemon_ou_pb2_grpc.gameserverStub(channel)  # create stub
            res = stub.Connect(pokemon_ou_pb2.ConnectMessage(type = 'poke')) # connect to server indicating pokemon as type
            self.name = res.status # set name of pokemon
            self.path.append(res.pos) # add starting position to path

            caught = 0 # 0 = not caught, 1 = caught
            time.sleep(8) # wait 8 seconds for other nodes to connect
            while(caught!=1): # while pokemon is not caught
                res = stub.BoardCheck(pokemon_ou_pb2.CurrentLocation(type = 'poke', location = self.path[-1])) # check board for possible moves
                if (len(res.starmoves) > 0): # if there are preferred moves
                    move = int(res.starmoves[random.randint(0,len(res.starmoves)-1)]) # choose a random preferred move
                elif(len(res.moves) > 0): # if there are no preferred moves, but there are other moves
                    move = int(res.moves[random.randint(0,len(res.moves)-1)]) # choose a random move
        
                moveResponse = stub.MoveRequest(pokemon_ou_pb2.MoveRequestMessage(type = 'poke', name = self.name, move = move, curr = self.path[-1])) # request move
                   
                if moveResponse.status != 'no': # if move was successful
                        self.path.append(move) # add move to path
                if moveResponse.status == 'Captured': # if pokemon was captured
                        caught = 1 # set caught to 1 and end loop 

            res = stub.isGameOver(pokemon_ou_pb2.Empty()) # check if game is over
            while(res.status == 'no'): # while game is not over
                time.sleep(2) # wait 2 seconds
                res = stub.isGameOver(pokemon_ou_pb2.Empty()) # check if game is over again
            stub.passInfo(pokemon_ou_pb2.Info(path = self.path,name = self.name, dex = [])) # game is over now, pass path, and name to server


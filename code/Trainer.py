import pokemon_ou_pb2
import pokemon_ou_pb2_grpc
import grpc
import time
import random

class Trainer:
    name = "" # name
    path = [] # array of moves taken
    pokedex = [] # array of pokemon caught

    def Path(self): 
        return self.path 

    def Pokedex(self):
        return self.pokedex

    def __init__(self):
        with grpc.insecure_channel('server:50051') as channel:  # connect to server
            stub = pokemon_ou_pb2_grpc.gameserverStub(channel) # create stub
            res = stub.Connect(pokemon_ou_pb2.ConnectMessage(type = 'train')) # connect to server indicating trainer as type
            self.name = res.status # set name of trainer
            self.path.append(res.pos) # add starting position to path
            gameOver = 'no' # game is not over
            time.sleep(10) # wait 10 seconds for other nodes to connect (pokemon will connect and move first)
            while gameOver == 'no': # while game is not over
                res = stub.BoardCheck(pokemon_ou_pb2.CurrentLocation(type = 'train', location = self.path[-1])) # check board for possible moves
                if (len(res.starmoves) > 0): # if a preferred move is available
                    move = int(res.starmoves[random.randint(0,len(res.starmoves)-1)]) # choose a random preferred move
                elif(len(res.moves) > 0): # if there are no preferred moves, but there are other moves
                     move = int(res.moves[random.randint(0,len(res.moves)-1)]) # choose a random move
                   
                moveResponse = stub.MoveRequest(pokemon_ou_pb2.MoveRequestMessage(type = 'train', name = self.name, move = move, curr = self.path[-1])) # request move
                if moveResponse.status != 'no': # if move was successful
                        self.path.append(move) # add move to path
                if moveResponse.status == 'poke': # if the move was to a space occupied by a pokemon (or multiple pokemon)
                        res = stub.Capture(pokemon_ou_pb2.CaptureReq(pos = self.path[-1])) # request pokemon to be captured
                        if(len(res.names) > 0): # if pokemon were captured
                            for pokemon in res.names: # for each pokemon captured
                                self.pokedex.append(pokemon) # add pokemon to pokedex

                gameOver = stub.isGameOver(pokemon_ou_pb2.Empty()).status # check if game is over
            stub.passInfo(pokemon_ou_pb2.Info(path = self.path,name = self.name, dex = self.pokedex)) # game is over now, pass path, name, and pokedex to server
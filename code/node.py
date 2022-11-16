import socket
import time
import pokemon_ou_pb2
import pokemon_ou_pb2_grpc
import grpc
import random
import sys
import concurrent.futures
import sys
from Pokemon import Pokemon
from Trainer import Trainer

class space:
    def __init__(self):
        self.occupied = False
        self.pokemon = [] 
        self.trainer = None

class gameserver(pokemon_ou_pb2_grpc.gameserverServicer):
    def __init__(self):
        self.animals = ['🐕', '🐈', '🐁', '🐹', '🐰', '🐺', '🐸', '🐯', '🐨', '🐻', '🐷', '🐽', '🐮', '🐗', '🐵', '🐒', '🐴', '🐎', '🐫', '🐑', '🐘', '🐼', '🐍', '🐦', '🐤', '🐥', '🐣', '🐔', '🐧', '🐢', '🐛', '🐝', '🐜', '🐞', '🐌', '🐙', '🐠', '🐟', '🐳', '🐋', '🐬', '🐄', '🐏', '🐀', '🐃', '🐅', '🐇', '🐉', '🐐', '🐓', '🐕', '🐖', '🐁', '🐂', '🐲', '🐡', '🐡', '🐊', '🐪', '🐆', '🐈', '🐩', '🐾', '💐', '🌸', '🌷', '🍀', '🌹', '🌻', '🌺', '🌿', '🌾', '🍄', '🌵', '🌴', '🌲', '🌳', '🌰', '🌱', '🌼', '🌐', '🌞', '🌝', '🌚', '🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘', '🌙', '🌜', '🌛', '🌔', '🌍', '🌎', '🌏', '🌋', '🌌', ' ⛅️', '🐙', '🚢', '🐿']
        self.people = ["😀","😃","😄","😁","😆","😅","😂","🤣","☺️","😊","😇","🙂","🙃","😉","😌","😍","🥰","😘","😗","😙","😚","😋","😛","😝","😜","🤪","🤨","🧐","🤓","😎","🤩","🥳","😏","😒","😞","😔","😟","😕","🙁","☹️","😣","😖","😫","😩","🥺","😢","😭","😤","😠","😡","🤬","🤯","😳","🥵","🥶","😱","😨","😰","😥","😓","🤗","🤔","🤭","🤫","🤥","😶","😐","😑","😬","🙄","😯","😦","😧","😮","😲","🥱","😴","🤤","😪","😵","🤐","🥴","🤢","🤮","🤧","😷","🤒","🤕","🤑","🤠","😈","👿","👹","👺","💀","☠️","👻","👽","👾","🤖","💩","😺","😸","😹","😻","😼","😽","🙀","😿","😾"]
        self.pokecount = 0
        self.peoplecount = 0
        self.board = [] * (n*n)
        for i in range(n*n):
            self.board.append(space())
    def Captured(self, request, context):
        print('Captured')
        return pokemon_ou_pb2.CapturedMessage()

    def Moves(self, request, context):
        print('Moves')
        return pokemon_ou_pb2.MovesRecord()

    def Board(self, request, context):
        output = "\n"

        for i in range(n*n):
            if((i+1)%n==0):
                if(self.board[i].trainer!=None):
                    output += self.board[i].trainer
                elif(len(self.board[i].pokemon)>0):
                    output += self.board[i].pokemon[0]
                else:
                    output += "⬜"
                output += "\n"
            else:
                if(self.board[i].trainer!=None):
                    output += self.board[i].trainer
                elif(len(self.board[i].pokemon)>0):
                    output += self.board[i].pokemon[0]
                else:
                    output += "⬜"

        output+="\n"
        print(output)
        return pokemon_ou_pb2.Empty()


    def Connect(self, request, context):
        if(request.type == 'poke'):
            time.sleep(1)
            self.pokecount += 1
            name = self.animals[self.pokecount-1]
            x = random.randint(0,(n*n)-1)
            while(self.board[x].trainer!=None and len(self.board[x].pokemon)>0):
                x = random.randint(0,(n*n)-1)
                time.sleep(random.randint(0,2))
            while(self.board[x].trainer!=None and len(self.board[x].pokemon)>0):
                x = random.randint(0,(n*n)-1)
                time.sleep(random.randint(0,2))
            self.board[x].pokemon.append(name)
            return pokemon_ou_pb2.ConnectResponse(status = name, pos = x)
        else:
            time.sleep(.5)
            self.peoplecount += 1
            name = self.people[self.peoplecount-1]
            x = random.randint(0,(n*n)-1)
            while(self.board[x].trainer!=None and len(self.board[x].pokemon)>0):
                x = random.randint(0,(n*n)-1)
                time.sleep(random.randint(0,2))
            while(self.board[x].trainer!=None and len(self.board[x].pokemon)>0):
                x = random.randint(0,(n*n)-1)
                time.sleep(random.randint(0,2))
            self.board[x].trainer = name
            return pokemon_ou_pb2.ConnectResponse(status = name, pos = x)

    def MoveRequest(self, request, context):
        print('MoveRequest')
        return pokemon_ou_pb2.MoveRequestMessage()
    


def server():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    pokemon_ou_pb2_grpc.add_gameserverServicer_to_server(gameserver(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('Server started')
    try:
        while True:
            time.sleep(20)
            break
    except KeyboardInterrupt:
        server.stop(0)
        

if __name__== '__main__':
    curr = socket.gethostname()
    if curr == "Server":
        n = int(sys.argv[1])
        server()
    elif curr[0:7] == "Trainer":
        time.sleep(4)
        train = Trainer()
    elif curr[0:7] == "Pokemon":
        time.sleep(4)
        poke = Pokemon()

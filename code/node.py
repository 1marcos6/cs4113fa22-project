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
        output = ""

        for i in range(n*n):
            if((i+1)%n == 0):
                if((i+1) == n*n):
                    break
                output+='\n'

            else:
                if(self.board[i].trainer!=None):
                    output+=self.board[i].trainer
                else:
                    if(len(self.board[i].pokemon) ==0):
                        output+="⬜️"
                    else:
                        output+=self.board[i].pokemon[0]
        print(output)
        return pokemon_ou_pb2.Empty()


    def Connect(self, request, context):
        if(request.type == 'poke'):
            self.pokecount += 1
            name = self.animals[self.pokecount-1]
            return pokemon_ou_pb2.ConnectMessage(type = name)
        else:
            self.peoplecount += 1
            name = self.people[self.peoplecount-1]
            return pokemon_ou_pb2.ConnectMessage(type = name)

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

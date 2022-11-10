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

n = 0
class gameserver(pokemon_ou_pb2_grpc.gameserverServicer):
    def __init__(self):
        self.animals = ['🐕', '🐈', '🐁', '🐹', '🐰', '🐺', '🐸', '🐯', '🐨', '🐻', '🐷', '🐽', '🐮', '🐗', '🐵', '🐒', '🐴', '🐎', '🐫', '🐑', '🐘', '🐼', '🐍', '🐦', '🐤', '🐥', '🐣', '🐔', '🐧', '🐢', '🐛', '🐝', '🐜', '🐞', '🐌', '🐙', '🐠', '🐟', '🐳', '🐋', '🐬', '🐄', '🐏', '🐀', '🐃', '🐅', '🐇', '🐉', '🐐', '🐓', '🐕', '🐖', '🐁', '🐂', '🐲', '🐡', '🐡', '🐊', '🐪', '🐆', '🐈', '🐩', '🐾', '💐', '🌸', '🌷', '🍀', '🌹', '🌻', '🌺', '🌿', '🌾', '🍄', '🌵', '🌴', '🌲', '🌳', '🌰', '🌱', '🌼', '🌐', '🌞', '🌝', '🌚', '🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘', '🌙', '🌜', '🌛', '🌔', '🌍', '🌎', '🌏', '🌋', '🌌', ' ⛅️', '🐙', '🚢', '🐿']
        self.people = ["😀","😃","😄","😁","😆","😅","😂","🤣","☺️","😊","😇","🙂","🙃","😉","😌","😍","🥰","😘","😗","😙","😚","😋","😛","😝","😜","🤪","🤨","🧐","🤓","😎","🤩","🥳","😏","😒","😞","😔","😟","😕","🙁","☹️","😣","😖","😫","😩","🥺","😢","😭","😤","😠","😡","🤬","🤯","😳","🥵","🥶","😱","😨","😰","😥","😓","🤗","🤔","🤭","🤫","🤥","😶","😐","😑","😬","🙄","😯","😦","😧","😮","😲","🥱","😴","🤤","😪","😵","🤐","🥴","🤢","🤮","🤧","😷","🤒","🤕","🤑","🤠","😈","👿","👹","👺","💀","☠️","👻","👽","👾","🤖","💩","😺","😸","😹","😻","😼","😽","🙀","😿","😾"]
        self.pokecount = 0
        self.peoplecount = 0
        self.board = [0] * (n*n)

    def Captured(self, request, context):
        print('Captured')
        return pokemon_ou_pb2.CapturedMessage()

    def Moves(self, request, context):
        print('Moves')
        return pokemon_ou_pb2.MovesRecord()

    def Board(self, request, context):
        print('Board')
        return pokemon_ou_pb2.BoardRecord()

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
    
        
    



def server(n):
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

def train():
    with grpc.insecure_channel('server:50051') as channel:  
        stub = pokemon_ou_pb2_grpc.gameserverStub(channel)
        name = stub.Connect(pokemon_ou_pb2.ConnectMessage(type = 'train')).type
        trainer = Trainer()
        trainer.setName(name)

    

def poke():  
    with grpc.insecure_channel('server:50051') as channel:  
        stub = pokemon_ou_pb2_grpc.gameserverStub(channel)
        name = stub.Connect(pokemon_ou_pb2.ConnectMessage(type = 'poke')).type
        pokefella = Pokemon()
        pokefella.setName(name)
    

        

if __name__== '__main__':
    curr = socket.gethostname()
    if curr == "Server":
        n = int(sys.argv[1])
        server(n)
    elif curr[0:7] == "Trainer":
        time.sleep(4)
        train()
    elif curr[0:7] == "Pokemon":
        time.sleep(4)
        poke()
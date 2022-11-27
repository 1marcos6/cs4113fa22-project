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
import threading


class space:
    def __init__(self):
        self.occupied = False
        self.pokemon = [] 
        self.trainer = None

class gameserver(pokemon_ou_pb2_grpc.gameserverServicer):
    def __init__(self):
        self.animals = ['🐕', '🐈', '🐁', '🐹', '🐰', '🐺', '🐸', '🐯', '🐨', '🐻', '🐷', '🐽', '🐮', '🐗', '🐵', '🐒', '🐴', '🐎', '🐫', '🐑', '🐘', '🐼', '🐍', '🐦', '🐤', '🐥', '🐣', '🐔', '🐧', '🐢', '🐛', '🐝', '🐜', '🐞', '🐌', '🐙', '🐠', '🐟', '🐳', '🐋', '🐬', '🐄', '🐏', '🐀', '🐃', '🐅', '🐇', '🐉', '🐐', '🐓', '🐕', '🐖', '🐁', '🐂', '🐲', '🐡', '🐡', '🐊', '🐪', '🐆', '🐈', '🐩', '🐾', '💐', '🌸', '🌷', '🍀', '🌹', '🌻', '🌺', '🌿', '🌾', '🍄', '🌵', '🌴', '🌲', '🌳', '🌰', '🌱', '🌼', '🌐', '🌞', '🌝', '🌚', '🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘', '🌙', '🌜', '🌛', '🌔', '🌍', '🌎', '🌏', '🌋', '🌌', ' ⛅️', '🐙', '🚢', '🐿']
        self.people = ["😀","😃","😄","😁","😆","😅","😂","🤣","😊","😇","🙂","🙃","😉","😌","😍","🥰","😘","😗","😙","😚","😋","😛","😝","😜","🤪","🤨","🧐","🤓","😎","🤩","🥳","😏","😒","😞","😔","😟","😕","🙁","😣","😖","😫","😩","🥺","😢","😭","😤","😠","😡","🤬","🤯","😳","🥵","🥶","😱","😨","😰","😥","😓","🤗","🤔","🤭","🤫","🤥","😶","😐","😑","😬","🙄","😯","😦","😧","😮","😲","🥱","😴","🤤","😪","😵","🤐","🥴","🤢","🤮","🤧","😷","🤒","🤕","🤑","🤠","😈","👿","👹","👺","💀","👻","👽","👾","🤖","💩","😺","😸","😹","😻","😼","😽","🙀","😿","😾"]
        self.pokecount = 0
        self.peoplecount = 0
        self.board = [] * (n*n)
        self.boardLocks = [] * (n*n)
        for i in range(n*n):
            self.board.append(space())
        for i in range(n*n):
            self.boardLocks.append(threading.Lock())
    def Captured(self, request, context):
        print('Captured')
        return pokemon_ou_pb2.CapturedMessage()

    def Moves(self, request, context):
        print('Moves')
        return pokemon_ou_pb2.MovesRecord()

    def Board(self, request, context):
        self.print()  
        return pokemon_ou_pb2.Empty()


    def Connect(self, request, context):
        if(request.type == 'poke'):
            #time.sleep(1)
            self.pokecount += 1
            name = self.animals[self.pokecount-1]
            x = random.randint(0,(n*n)-1)
            self.boardLocks[x].acquire()
            if(self.board[x].trainer == None and len(self.board[x].pokemon) == 0):
                self.board[x].pokemon.append(name)
            else:
                self.boardLocks[x].release()
                while(self.board[x].trainer != None or len(self.board[x].pokemon) != 0):
                    x = random.randint(0,(n*n)-1)
                    self.boardLocks[x].acquire()
                    if(self.board[x].trainer == None and len(self.board[x].pokemon) == 0):
                        self.board[x].pokemon.append(name)
                        break
                    else:
                        self.boardLocks[x].release()
            self.boardLocks[x].release()
            return pokemon_ou_pb2.ConnectResponse(status = name, pos = x)
        else:
            #time.sleep(.5)
            self.peoplecount += 1
            name = self.people[self.peoplecount-1]
            x = random.randint(0,(n*n)-1)
            self.boardLocks[x].acquire()
            if(self.board[x].trainer == None and len(self.board[x].pokemon) == 0):
                self.board[x].trainer = name
            else:
                self.boardLocks[x].release()
                while(self.board[x].trainer != None or len(self.board[x].pokemon) != 0):
                    x = random.randint(0,(n*n)-1)
                    self.boardLocks[x].acquire()
                    if(self.board[x].trainer == None and len(self.board[x].pokemon) == 0):
                        self.board[x].trainer = name
                        break
                    else:
                        self.boardLocks[x].release()
            self.boardLocks[x].release()
            return pokemon_ou_pb2.ConnectResponse(status = name, pos = x)


    def MoveRequest(self, request, context):
        if(request.type == 'poke'):
            if(len(self.board[request.move].pokemon) == 0):
                self.boardLocks[request.move].acquire()
                self.board[request.move].pokemon.append(request.name)
                self.board[request.curr].pokemon.remove(request.name)
                self.boardLocks[request.move].release()
                return pokemon_ou_pb2.Feedback(status = "yes")
            else:
                return pokemon_ou_pb2.Feedback(status = "no")
        else:
            if(self.board[request.move].trainer == None):
                self.boardLocks[request.move].acquire()
                self.board[request.move].trainer = request.name
                self.board[request.curr].trainer = None
                self.boardLocks[request.move].release()
                return pokemon_ou_pb2.Feedback(status = "yes")
            else:
                return pokemon_ou_pb2.Feedback(status = "no")
    def BoardCheck(self, request, context):
        possibleMoves =[]
        if(request.type == 'poke'):
            x = request.location
            if(0<x-(n+1)<len(self.board) and len(self.board[x-(n+1)].pokemon) ==0 and self.board[x-(n+1)].trainer == None):
                possibleMoves.append(x-(n+1))
            if(0<x-(n)<len(self.board) and len(self.board[x-(n)].pokemon) ==0 and self.board[x-(n)].trainer == None):
                possibleMoves.append(x-(n))
            if(0<x-(n-1)<len(self.board) and len(self.board[x-(n-1)].pokemon) ==0 and self.board[x-(n-1)].trainer == None):
                possibleMoves.append(x-(n-1))
            if(0<x-1<len(self.board) and len(self.board[x-1].pokemon) ==0 and self.board[x-1].trainer == None):
                possibleMoves.append(x-1)
            if(0<x+1<len(self.board) and len(self.board[x+1].pokemon) ==0 and self.board[x+1].trainer == None):
                possibleMoves.append(x+1)
            if(0<x+(n-1)<len(self.board) and len(self.board[x+(n-1)].pokemon) ==0 and self.board[x+(n-1)].trainer == None):
                possibleMoves.append(x+(n-1))
            if(0<x+n<len(self.board) and len(self.board[x+(n)].pokemon) ==0 and self.board[x+(n)].trainer == None):
                possibleMoves.append(x+(n))
            if(0<x+(n+1)<len(self.board) and len(self.board[x+(n+1)].pokemon) ==0 and self.board[x+(n+1)].trainer == None):
                possibleMoves.append(x+(n+1))

        else:
            x = request.location
            if(0<x-(n)<len(self.board) and self.board[x-(n)].trainer == None):
                if(len(self.board[x-(n)].pokemon) > 0):
                    #insert at beginning of list
                    possibleMoves.insert(0,x-(n))
                else:
                    possibleMoves.append(x-(n))
            if(len(self.board[x-(n+1)].pokemon) > 0):
                    #insert at beginning of list
                    possibleMoves.insert(0,x-(n+1))
            else:
                    possibleMoves.append(x-(n+1))
            if(0<x-1<len(self.board) and self.board[x-1].trainer == None):
                if(len(self.board[x-1].pokemon) > 0):
                    #insert at beginning of list
                    possibleMoves.insert(0,x-1)
                else:
                    possibleMoves.append(x-1)
            if(0<x+1<len(self.board) and self.board[x+1].trainer == None):
                if(len(self.board[x+1].pokemon) > 0):
                    #insert at beginning of list
                    possibleMoves.insert(0,x+1)
                else:
                    possibleMoves.append(x+1)
            if(0<x+(n-1)<len(self.board) and self.board[x+(n-1)].trainer == None):
                if(len(self.board[x+(n-1)].pokemon) > 0):
                    #insert at beginning of list
                    possibleMoves.insert(0,x+(n-1))
                else:
                    possibleMoves.append(x+(n-1))
            if(0<x+n<len(self.board)  and self.board[x+(n)].trainer == None):
                if(len(self.board[x+(n)].pokemon) > 0):
                    #insert at beginning of list
                    possibleMoves.insert(0,x+(n))
                else:
                    possibleMoves.append(x+(n))

            if(0<x-(n-1)<len(self.board) and self.board[x-(n-1)].trainer == None):
                if(len(self.board[x-(n-1)].pokemon) > 0):
                    #insert at beginning of list
                    possibleMoves.insert(0,x-(n-1))
                else:
                    possibleMoves.append(x-(n-1))
                    
            if(0<x+(n+1)<len(self.board)  and self.board[x+(n+1)].trainer == None):
                if(len(self.board[x+(n+1)].pokemon) > 0):
                    #insert at beginning of list
                    possibleMoves.insert(0,x+(n+1))
                else:
                    possibleMoves.append(x+(n+1))
        return pokemon_ou_pb2.PossibleMoves(moves = possibleMoves)

    def print(self):
        output = ""

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

        output+='\n'
        print(output)
    


def server():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    servicer = gameserver()
    pokemon_ou_pb2_grpc.add_gameserverServicer_to_server(servicer, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('Server started')
    try:
        #print('\n')
        print('\033[H\033[J')
        print('\033[H\033[J')

        while True:
            print('\033[H')
            servicer.print()
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
